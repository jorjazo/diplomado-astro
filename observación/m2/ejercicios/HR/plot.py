import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.gaia import Gaia
import time
import os

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

USAR_LOGIN = False
GAIA_USER = os.environ.get('GAIA_USER', '')
GAIA_PASS = os.environ.get('GAIA_PASS', '')

# Parámetros
TOL_MATCH_FILTROS = 3.0        # arcsec, cruce B/G/R
TOL_MATCH_GAIA_INICIAL = 5.0   # arcsec, primer cruce con Gaia (tolerante al sesgo)
TOL_MATCH_GAIA_FINAL = 1.5     # arcsec, segundo cruce tras corregir sesgo
MARGEN_CAMPO_DEG = 0.05        # margen extra al descargar Gaia (~3')
MAG_GAIA_MAX = 18              # filtrar estrellas Gaia muy débiles (irrelevantes)

# Filtros de miembros
SNR_PARALAJE_MIN = 3
DIST_M6_MIN = 350
DIST_M6_MAX = 700
TOL_MOV_PROPIO = 3.0

# ====================================================================

t_inicio = time.time()
def log_t(etapa, t_prev):
    t_ahora = time.time()
    print(f"  ⏱  {etapa}: {t_ahora - t_prev:.2f}s (total: {t_ahora - t_inicio:.2f}s)")
    return t_ahora
t = t_inicio

# === Login ===
if USAR_LOGIN and GAIA_USER and GAIA_PASS:
    print("Iniciando sesión en Gaia...")
    Gaia.login(user=GAIA_USER, password=GAIA_PASS)
    t = log_t("Login", t)

# === 1. Cargar CSV ===
B = pd.read_csv('B.csv')
G = pd.read_csv('G.csv')
R = pd.read_csv('R.csv')
print(f"Estrellas iniciales: B={len(B)}, G={len(G)}, R={len(R)}")
t = log_t("Carga CSV", t)

# === 2. Limpieza ===
def limpiar(df):
    fwhm_med = df['FWHMx'].median()
    return df[
        (df['RMSE'] < 0.05) &
        (df['FWHMx'] < 2 * fwhm_med) &
        (df['FWHMy'] < 2 * fwhm_med) &
        (df['FWHMx'] > 0.5 * fwhm_med)
    ].reset_index(drop=True)

B = limpiar(B); G = limpiar(G); R = limpiar(R)
print(f"Tras limpieza:       B={len(B)}, G={len(G)}, R={len(R)}")
t = log_t("Limpieza", t)

# === 3. Cruce entre filtros B, G, R ===
tol = TOL_MATCH_FILTROS * u.arcsec
coords_G = SkyCoord(ra=G['Ra'].values*u.deg, dec=G['Dec'].values*u.deg)
coords_B = SkyCoord(ra=B['Ra'].values*u.deg, dec=B['Dec'].values*u.deg)
coords_R = SkyCoord(ra=R['Ra'].values*u.deg, dec=R['Dec'].values*u.deg)

idx_B, sep_B, _ = coords_G.match_to_catalog_sky(coords_B)
idx_R, sep_R, _ = coords_G.match_to_catalog_sky(coords_R)
match = (sep_B < tol) & (sep_R < tol)

mag_G = G['Mag'].values[match]
mag_B = B['Mag'].values[idx_B[match]]
mag_R = R['Mag'].values[idx_R[match]]
coords_match = coords_G[match]
print(f"Estrellas con match en los 3 filtros: {match.sum()}")
t = log_t("Cruce de filtros", t)

# === 4. Diagnóstico del campo observado ===
ra_med = np.median(coords_match.ra.deg)
dec_med = np.median(coords_match.dec.deg)
ra_min, ra_max = coords_match.ra.deg.min(), coords_match.ra.deg.max()
dec_min, dec_max = coords_match.dec.deg.min(), coords_match.dec.deg.max()

print(f"\n=== CAMPO OBSERVADO ===")
print(f"Centro detectado: RA={ra_med:.4f}°, Dec={dec_med:.4f}°")
print(f"Centro M6 SIMBAD: RA=265.0833°, Dec=-32.2333°")
print(f"Rango: RA [{ra_min:.4f}, {ra_max:.4f}], Dec [{dec_min:.4f}, {dec_max:.4f}]")
print(f"Tamaño: {(ra_max-ra_min)*np.cos(np.radians(dec_med)):.3f}° x {dec_max-dec_min:.3f}°")

# === 5. Una sola consulta a Gaia: descargar todo el campo ===
print("\nDescargando catálogo Gaia DR3 del campo completo...")
t_q = time.time()

# Ampliar un poco la caja para no perder estrellas del borde
ra_lo = ra_min - MARGEN_CAMPO_DEG / np.cos(np.radians(dec_med))
ra_hi = ra_max + MARGEN_CAMPO_DEG / np.cos(np.radians(dec_med))
dec_lo = dec_min - MARGEN_CAMPO_DEG
dec_hi = dec_max + MARGEN_CAMPO_DEG

query = f"""
SELECT
    source_id, ra, dec, parallax, parallax_error,
    pmra, pmdec, phot_g_mean_mag, bp_rp
FROM gaiadr3.gaia_source
WHERE ra BETWEEN {ra_lo} AND {ra_hi}
  AND dec BETWEEN {dec_lo} AND {dec_hi}
  AND phot_g_mean_mag < {MAG_GAIA_MAX}
"""
job = Gaia.launch_job_async(query)
gaia_full = job.get_results().to_pandas()
print(f"Estrellas Gaia descargadas: {len(gaia_full)}")
print(f"Rango de mag G en Gaia: {gaia_full['phot_g_mean_mag'].min():.2f} a {gaia_full['phot_g_mean_mag'].max():.2f}")
t = log_t("Consulta Gaia única", t_q)

# === 6. Primer match con tolerancia grande (5") ===
print(f"\nPrimer cruce con tolerancia de {TOL_MATCH_GAIA_INICIAL}\"...")
coords_gaia = SkyCoord(ra=gaia_full['ra'].values*u.deg, dec=gaia_full['dec'].values*u.deg)
idx_g1, sep_g1, _ = coords_match.match_to_catalog_sky(coords_gaia)
match1 = sep_g1 < TOL_MATCH_GAIA_INICIAL * u.arcsec
print(f"Matches encontrados: {match1.sum()} de {len(coords_match)}")

# === 7. CORRECCIÓN DEL SESGO ASTROMÉTRICO ===
# Si hay un desplazamiento sistemático entre tu plate-solve y Gaia,
# se ve como mediana no-cero en (ra_tuya - ra_gaia) y (dec_tuya - dec_gaia).
# Lo medimos usando solo estrellas brillantes en Gaia (más confiables).

# Para estimar el sesgo, usar matches donde la estrella Gaia sea brillante
gaia_brillantes_mask = gaia_full['phot_g_mean_mag'].values[idx_g1[match1]] < 14
if gaia_brillantes_mask.sum() < 5:
    # Si hay pocas brillantes, usar todas las matcheadas
    gaia_brillantes_mask = np.ones(match1.sum(), dtype=bool)

idx_g_match = idx_g1[match1]
delta_ra_arcsec  = (coords_match[match1].ra.deg  - gaia_full['ra'].values[idx_g_match]) * 3600 * np.cos(np.radians(dec_med))
delta_dec_arcsec = (coords_match[match1].dec.deg - gaia_full['dec'].values[idx_g_match]) * 3600

sesgo_ra  = np.median(delta_ra_arcsec[gaia_brillantes_mask])
sesgo_dec = np.median(delta_dec_arcsec[gaia_brillantes_mask])
print(f"\n=== SESGO ASTROMÉTRICO DETECTADO ===")
print(f"Δ RA  (tuya − Gaia): {sesgo_ra:+.2f}\"")
print(f"Δ Dec (tuya − Gaia): {sesgo_dec:+.2f}\"")
print(f"Magnitud del sesgo: {np.sqrt(sesgo_ra**2 + sesgo_dec**2):.2f}\"")

# === 8. Aplicar corrección y rematchar con tolerancia estricta ===
ra_corregida  = coords_match.ra.deg  - sesgo_ra  / 3600 / np.cos(np.radians(dec_med))
dec_corregida = coords_match.dec.deg - sesgo_dec / 3600
coords_corregida = SkyCoord(ra=ra_corregida*u.deg, dec=dec_corregida*u.deg)

print(f"\nSegundo cruce con tolerancia de {TOL_MATCH_GAIA_FINAL}\" tras corrección...")
idx_g2, sep_g2, _ = coords_corregida.match_to_catalog_sky(coords_gaia)
match2 = sep_g2 < TOL_MATCH_GAIA_FINAL * u.arcsec
print(f"Matches encontrados: {match2.sum()} de {len(coords_match)}")
t = log_t("Matching con corrección", t)

# === 9. Construir DataFrame final ===
idx_local = np.where(match2)[0]
idx_gaia  = idx_g2[match2]
sep_final = sep_g2[match2].arcsec

gaia_df = gaia_full.iloc[idx_gaia].copy().reset_index(drop=True)
gaia_df['local_id'] = idx_local
gaia_df['sep_arcsec'] = sep_final

# === 10. Diagnóstico ===
print("\n" + "="*60)
print("DIAGNÓSTICO DE DATOS GAIA")
print("="*60)
print("\n📏 Separación angular post-corrección (arcsec):")
print(gaia_df['sep_arcsec'].describe().to_string())

print("\n🔭 Paralajes (mas):")
print(gaia_df['parallax'].describe().to_string())

print("\n📊 S/N de paralaje:")
snr = gaia_df['parallax'] / gaia_df['parallax_error']
print(snr.describe().to_string())

print("\n✨ Magnitudes G de Gaia matcheadas:")
print(gaia_df['phot_g_mean_mag'].describe().to_string())

dist_cruda = 1000.0 / gaia_df.loc[gaia_df['parallax'] > 0, 'parallax']
print(f"\n🎯 Distancias crudas (parallax > 0):")
print(f"  Mediana: {dist_cruda.median():.0f} pc")
print(f"  Estrellas a {DIST_M6_MIN}-{DIST_M6_MAX} pc: {((dist_cruda > DIST_M6_MIN) & (dist_cruda < DIST_M6_MAX)).sum()}")
print("="*60)

# === 11. Filtros y cálculos finales ===
gaia_df = gaia_df.dropna(subset=['parallax']).copy()
gaia_df = gaia_df[
    (gaia_df['parallax'] > 0) &
    (gaia_df['parallax'] / gaia_df['parallax_error'] > SNR_PARALAJE_MIN)
].reset_index(drop=True)
print(f"\nCon paralaje confiable (S/N > {SNR_PARALAJE_MIN}): {len(gaia_df)}")

gaia_df['dist_pc'] = 1000.0 / gaia_df['parallax']

idx_validos = gaia_df['local_id'].values.astype(int)
mag_G_inst = mag_G[idx_validos]
mag_B_inst = mag_B[idx_validos]

zp = np.median(gaia_df['phot_g_mean_mag'].values - mag_G_inst)
print(f"Punto cero estimado para G: {zp:.2f}")
mag_G_cal = mag_G_inst + zp
mag_G_abs = mag_G_cal - 5 * np.log10(gaia_df['dist_pc'].values / 10)
color_BG = mag_B_inst - mag_G_inst

cerca_M6 = (gaia_df['dist_pc'] > DIST_M6_MIN) & (gaia_df['dist_pc'] < DIST_M6_MAX)
print(f"Estrellas en rango [{DIST_M6_MIN},{DIST_M6_MAX}] pc: {cerca_M6.sum()}")

if cerca_M6.sum() > 3:
    pmra_c = gaia_df.loc[cerca_M6, 'pmra'].median()
    pmdec_c = gaia_df.loc[cerca_M6, 'pmdec'].median()
    print(f"Movimiento propio del cúmulo (auto): pmRA={pmra_c:.2f}, pmDec={pmdec_c:.2f}")
else:
    pmra_c, pmdec_c = -1.5, -2.5
    print(f"⚠ Fallback: pmRA={pmra_c}, pmDec={pmdec_c}")

miembros = (
    (np.abs(gaia_df['pmra'].values - pmra_c) < TOL_MOV_PROPIO) &
    (np.abs(gaia_df['pmdec'].values - pmdec_c) < TOL_MOV_PROPIO) &
    cerca_M6.values
)
print(f"Miembros probables de M6: {miembros.sum()}")
t = log_t("Procesado final", t)

# === 12. Gráficos ===
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

axes[0].scatter(color_BG, mag_G_abs, s=14, alpha=0.4, color='gray', label='Campo')
axes[0].scatter(color_BG[miembros], mag_G_abs[miembros], s=24, alpha=0.9,
                color='steelblue', edgecolor='k', linewidth=0.3, label='Miembros M6')
axes[0].invert_yaxis()
axes[0].set_xlabel('B − G (color instrumental)')
axes[0].set_ylabel('M_G (magnitud absoluta calibrada)')
axes[0].set_title('CMD con distancia + ZP calibrado')
axes[0].legend(); axes[0].grid(alpha=0.3)

axes[1].hist(gaia_df['dist_pc'].values, bins=40, alpha=0.5, color='gray',
             label='Todas', range=(0, 3000))
axes[1].hist(gaia_df['dist_pc'].values[miembros], bins=40, alpha=0.8,
             color='steelblue', label='Miembros M6', range=(0, 3000))
axes[1].axvline(487, color='red', linestyle='--', label='M6 (~487 pc)')
axes[1].set_xlabel('Distancia (pc)'); axes[1].set_ylabel('N estrellas')
axes[1].set_title('Distribución de distancias')
axes[1].legend(); axes[1].grid(alpha=0.3)

axes[2].scatter(gaia_df['pmra'], gaia_df['pmdec'], s=14, alpha=0.4, color='gray', label='Todas')
axes[2].scatter(gaia_df.loc[miembros, 'pmra'], gaia_df.loc[miembros, 'pmdec'],
                s=24, alpha=0.9, color='steelblue', edgecolor='k', linewidth=0.3,
                label='Miembros M6')
axes[2].axvline(pmra_c, color='red', linestyle=':', alpha=0.5)
axes[2].axhline(pmdec_c, color='red', linestyle=':', alpha=0.5)
axes[2].set_xlabel('pmRA (mas/yr)'); axes[2].set_ylabel('pmDec (mas/yr)')
axes[2].set_title('Espacio de movimientos propios')
axes[2].legend(); axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('M6_CMD_gaia.png', dpi=150)
plt.show()
print("\nGuardado: M6_CMD_gaia.png")
t = log_t("Gráficos", t)

print(f"\n{'='*60}")
print(f"⏱  TIEMPO TOTAL: {time.time() - t_inicio:.2f}s")
print(f"{'='*60}")

if USAR_LOGIN and GAIA_USER:
    Gaia.logout()

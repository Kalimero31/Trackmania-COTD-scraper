import TrackManiaCOTDScraping as TMScrap

# 19th of october 2023 COTD
#================
COTD_ID = 10811 
#================

# Save the COTD data: 
df = TMScrap.scrap_COTD(COTD_ID)

df.to_csv('data-COTD/COTD_'+ str(COTD_ID) + '.csv', index=False)



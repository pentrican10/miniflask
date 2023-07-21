from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

fits_file600 = fits.open('S00600_lc_detrended.fits')


x_600 = fits_file600[1].data
y_600 = fits_file600[2].data

#plot
plt.plot(x_600, y_600, label='Flux vs Time')
plt.title('Kepler Detrended Light Curve S00600')
plt.legend()
plt.xlabel('Time (days)')
plt.ylabel('Flux')
plt.show()
#figure
df = pd.DataFrame(dict(
    TIME=x_600,
    FLUX=y_600
))
fig = px.scatter(df, x="TIME", y="FLUX", 
                 title="Kepler Detrended Light Curve S00600")
fig.show()


new_comment = input('Write comments on detrended light curve here(include number): ')

comments = open('kepler_comments.txt', 'a')
comments.write(str(new_comment)+'\n')
#comments.write('\n')
comments.close()

comments = open('kepler_comments.txt','r')
print("The comments file reads: ")
print(comments.readlines())
comments.close()


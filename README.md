# photoZ

This script is what I use to estimate the redshift of the source galaxy in strongly lensed galaxy-galaxy systems. It uses the pre-made templates based on Benitez et al. 2000, which I make available at: 

https://www.dropbox.com/sh/3r4z4cfjvn15k77/AABnnd4NvzSJ9RB4TVT05aNxa?dl=0

(one needs to download these templates to the main directory of the code. a simple download of the whole dropbox directory, which contains the scripts as well, is sufficient)
By default, it is optimized to run on 50 cores, but one can change that easily in estimateMulticore123.py and photoz.csh. 

---
This is a Bayesian likelihood estimator of photometric redshift. Given 5-band magnitude measurements, with the corresponding error bars in data.txt, this code calculates the redshift PDF for each galaxy and compares it with the spectroscopic redshift. 

The data.txt, which is the input file, is organized as follows: 
1st row: ID<br>
2nd row: g-band magnitude 
3rd row: g-band uncertainty
4th row: r-band magnitude
5th row: r-band uncertainty
7th row: i-band mag
8th row: i-band uncertainty
9th row: z-band mag
10th row: z-band uncertainty
11th row: y-band mag
12th row: y-band uncertainty
13th row: spectroscopic redshift (for comparison purposes)

These galaxies are selected from HSC public data release, with 1<z<3. The data.txt file contains 200 galaxies. 

---
to run the code: 
```
bash photoz.csh 
```
or preferably(to be able to kill the process if anything went wrong)  screen it via:
```
screen -S photoz -dm bash photoz.csh
```

Outputs will be saved in 'probPlots' and 'outputs' directories which will be produced after running the code. The output folder will contain .pickle files for later analytic purposes. The probPlots folder will contain:

the redshift PDF for each galaxy as galaxyID.pdf
numerical redshift PDF for each galaxy as galaxyID.txt
estimated photometric redshifts plotted against spectroscopic redshifts as wrap.txt
outlier.txt containing the outlier fraction and the first sigma of the experiment

Outliers are defined as abs(spectroscopic redshift - photometric redshift)/(1+spectroscopic redshift)>0.15. The first sigma and outlier fraction are defined similar to Tanaka et al. 2017 (https://arxiv.org/abs/1704.05988). 

---
For more information, refer to the thesis at: 

https://github.com/rangavar/photoZ/raw/master/Photometric_Redshift_Estimation_of_Strongly_Lensed_Galaxies.pdf



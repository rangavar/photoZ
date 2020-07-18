mkdir outputs #folder to save .pickle outputs, containing the full calculated likelihood space
mkdir probPlots #folder to save the probability distribution function for each object

python estimateMulticore.py #produce multiple copies of the core (50 copies in this setting) to make it possible to run the code on 50 cores parallel

#run the aformentioned codes (which are saved as $i$core.py at the same time
for i in {0..49};do
	python ${i}core.py &
done
wait

cp 68percentile.py probPlots/
#plotting: go through the (previously known) spectroscopic redshifts and the calculated photometric (this is what we calculated here) redshifts and plot them against each other
cd probPlots/
python 68percentile.py

for i in 1 2
do
	python3 monotonical_change_ALL_IN_ONE.py 3 /research/labs/surgresearch/jsung/m221138/RA_project/analysis/etc/class3 3 $i &
	python3 monotonical_change_ALL_IN_ONE.py 4 /research/labs/surgresearch/jsung/m221138/RA_project/analysis/etc/class4 3 $i &
done

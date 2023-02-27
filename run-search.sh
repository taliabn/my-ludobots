for SEED in 86 256 404 505 672 101 18 808 45 37
do
	python search.py $SEED > out$SEED.txt 2>&1
	echo "FINISHED SEED $SEED"
done
echo "FINISHED ALL"


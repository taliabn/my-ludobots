for SEED in 404 86 505 672 101
do
	python search.py $SEED > out$SEED.txt 2>&1
	echo "FINISHED SEED $SEED"
	sleep 60s
done
echo "FINISHED ALL"


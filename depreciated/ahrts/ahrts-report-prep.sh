list_of_diffs=$1
if [[ -z $2 ]] ;then
	output_file=/dev/null
else
	output_file=$2
fi

v1=6.0mr1
v2=6.0mr1e
test_output_path=/mnt/storage/test-cases/newstuff
compare_output_path=/mnt/storage/test-cases/compare_results

for i in `sed "s/ /;;;/g" ${list_of_diffs}` ;do
	l=${i//;;;/ }
	n=${l//*\//}
	d=${test_output_path}/${n}/${n}
	mupdf ${d}*${v1}.pdf &
	mu1pid=$!
	mupdf ${d}*${v2}.pdf &
	mu2pid=$!
	gthumb ${compare_output_path}/${n} &
	gthum_pid=$!
	read comment
	kill -9 $mu1pid $mu2pid $gthum_pid
	if [[ $comment == '' ]] ;then 
		comment=$last_comment
	fi
	echo $comment $l >> $output_file
	last_comment=$comment
done

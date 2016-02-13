dir="$1"

for i in $dir/* ;do
	mv "$i" "$dir/${dir}.$(echo $(basename "$i") | tr "[!\"\`,?+=;:| ]" "." | tr -d "[\',{}[]()]"  | tr "&" "and" | tr [A-Z] [a-z])"
done

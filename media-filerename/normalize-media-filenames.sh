dir="$1"

for i in $dir/* ;do
	mv "$i" "$dir/$(echo $(basename "$i") | sed 's/ - /./g' | tr "[!\"\`,?+=;:| ]" "." | tr -d "[\',{}[]()]"  | tr "&" "and" | tr [A-Z] [a-z] | sed 's/\.\././g')"
done

#!/usr/bin/python

pages = 5000000

letter = 'A'

fotop = '''<?xml version="1.0" encoding="utf-8"?>

<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"
	xmlns:axf="http://www.antennahouse.com/names/XSL/Extensions"
	xmlns:m="http://www.w3.org/1998/Math/MathML"
	font-size="20pt">

	<axf:document-info name="title" value="Template Example" />

	<axf:document-info name="subject" value="Example" />

	<axf:document-info name="author" value="Chris Koepke" />

	<axf:document-info name="keywords" value="Example" />

	<fo:layout-master-set>

		<fo:simple-page-master page-width="8.5in" page-height="11in" margin="0in"
			master-name="PageMaster">

			<fo:region-body margin="20mm 20mm 20mm 20mm" />

		</fo:simple-page-master>

	</fo:layout-master-set>

	<fo:page-sequence master-reference="PageMaster">

		<fo:flow flow-name="xsl-region-body">'''

fobottom='''		</fo:flow>

	</fo:page-sequence>

</fo:root>'''

fomiddle='			<fo:block font-family="Arial" font-size="8pt" id="%ID%">SPAM!! SPAM!!! SPAM!!!!</fo:block>'



fotoc = '			<fo:block>Spam <fo:page-number-citation ref-id="%ID%" /></fo:block>\n'


foindex = '			<fo:block>Spam <fo:page-number-citation ref-id="%ID%" /></fo:block>\n'

toc = []

idnum = 0

count = 0

while idnum < pages:

	idnum += 1

	idstr = letter+str(idnum)

	toc.append(idstr)

print(fotop)

for i in toc:

	print(fotoc.replace('%ID%',i))

for i in toc:

        print(fomiddle.replace('%ID%',i))

	c = 0

	while c < 9:

        	print(fomiddle.replace('%ID%',i+'I'+str(c)))

		c += 1
 
for i in toc:

        print(foindex.replace('%ID%',i))

print(fobottom)

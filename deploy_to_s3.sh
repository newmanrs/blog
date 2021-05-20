#Build site
hugo
#Below copies all files... beware if site gets big.
aws s3 sync public/ s3://richmondnewman.com

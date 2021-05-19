./patch_theme.sh
hugo
aws s3 sync public/ s3://richmondnewman.com

echo "syncing built files directly to Amazon.  Note that this script neither 1) Builds, or 2) Removes files from the existing build directory, so files from prior builds that have not been overwritten are being staged.  Consider doing rm -r public/, then hugo build in this script for an all in one for safety?  Good thing this is a personal website so all this is irrelevant"
#s3cmd put -P --recursive ./public/ s3://richmondnewman.com
s3cmd sync ./public/ s3://richmondnewman.com

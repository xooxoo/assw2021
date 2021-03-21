#!/bin/bash

out_dir="data/data_glo"
month=06
year=2010
echo "login:"
read login
read -s -p "password: " pwd

for year in {2010..2020}
do
    out_name="glo_$year.nc"
    python -m motuclient --motu http://my.cmems-du.eu/motu-web/Motu --service-id GLOBAL_REANALYSIS_PHY_001_030-TDS --product-id global-reanalysis-phy-001-030-monthly --longitude-min -180 --longitude-max 179.9166717529297 --latitude-min 68 --latitude-max 90 --date-min "$year-06-15" --date-max "$year-10-16" --depth-min 0.493 --depth-max 9.574 --variable so --variable thetao --out-dir $out_dir --out-name $out_name --user $login --pwd $pwd
    echo $year
done

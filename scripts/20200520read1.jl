# author: Dylan Festa
# Goal : save data as HDF5
# work in progress

using DataFrames, CSV

## Read some data
datafile_retro_raw = abspath(joinpath(@__DIR__,"..","data/raw","0515RETROSPECTIVE.csv"))
@assert isfile(datafile_retro_raw)
dfretro_raw = CSV.read(datafile_retro_raw)
select!(dfretro_raw,Not("Study member"))

datafile_retro=abspath(joinpath(@__DIR__,"..","data/confidential","retrospective.csv"))
@assert isfile(datafile_retro)
dfretro=CSV.read(datafile_retro)

datafile_keyconv=abspath(joinpath(@__DIR__,"..","data/confidential","keys_list.csv"))
@assert isfile(datafile_keyconv)
dfkeysconv = CSV.read(datafile_keyconv)

keysretro_raw=names(dfretro_raw)
## test:  are the keys of the dictionary in the data?
dfkeysconv_missing = let nm=names(dfretro_raw)
    filter( k -> !in(k,nm),dfkeysconv.key_raw)
end
@assert isempty(dfkeysconv_missing)
# all good!
## test: which keys in the data are missing from the dictionary?
raw_keys_missing = filter( k -> !in(k,dfkeysconv.key_raw),keysretro_raw)
@assert isempty(raw_keys_missing)
# none ! cool! all test passed.

## Rename raw data with new column names
@assert ncol(dfretro) == nrow(dfkeysconv)

dfretro_out = copy(dfretro)
names(dfkeysconv)
for r in eachrow(dfkeysconv)
    rename!(dfretro_out, r.key_raw => r.key_new)
end

datafile_retro_sav = abspath(joinpath(@__DIR__,"..","data/raw","0515RETROSPECTIVE_rename.csv"))
CSV.write(datafile_retro_sav,dfretro_out)

## let's save a csv for the comments !

dfkeysconv_sorted = sort(dfkeysconv,:key_new)
dfkeysconv_sorted[:,:comment] .= "TO-DO"

CSV.write("/tmp/tmp.csv",dfkeysconv_sorted)


## Part 2 ! Check the other dataset !

datafile_eap = abspath(joinpath(@__DIR__,"..","data/raw","0516EAP.csv"))
@assert isfile(datafile_eap)
dfeap_raw = CSV.read(datafile_eap)
for n in names(dfeap_raw)
    @info n
end

# for each entry, find the 3 closest entries in the retro data, either edited or raw

pkg"add StringDistances"
using StringDistances

nm_eaps = names(dfeap_raw)
nm_retro = names(dfretro)
nm_retro_raw =names(dfretro_raw)

saymyname = map(nm_eaps) do nm
    cfun(s) = compare(s,nm,Partial(Levenshtein()))
    dists_retro = sort(nm_retro ; by=cfun,rev=true)[1:5]
    dists_retro_raw = sort(nm_retro_raw ; by=cfun,rev=true)[1:5]
    return (nm,join(dists_retro," : "),join(dists_retro_raw," : "))
end

dfeapnames = DataFrame(
    eap_label = getindex.(saymyname,1) ,
    retro_label = getindex.(saymyname,2) ,
    retro_raw_label = getindex.(saymyname,3) )

CSV.write("tmp.csv",dfeapnames)

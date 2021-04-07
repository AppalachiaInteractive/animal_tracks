
# Animal Tracks
A collection of graphics and images of animal tracks.  No attribution is required, do what you like.  I would love to see anything that you produce, though!  

*If you work for a conservation, fish, wildlife, parks, or similar service and need help using these, I'd be happy to donate my help.*

## Included
- PNG files of initial track silhouette
- SVG files of the track outline
- PNG file of a high-quality silhouette
- PNG files of *my estimation* of the track's surface details, such as displacement and surface normals.  

These are not scans - everything is derived from reference images, so they may not line up 100% with real world tracks.  Feel free to make pull requests if you can improve or add something. Raise issues if you would like an animal added or modified.  If you can provide the track silhouette and dimensions, even better.  No guarantees but I'll do what I can.  If you want to have a crack on your own, follow the process below.

### Process
Once a silhouette for a track is obtained:
- A subdirectory named for the animal is created in the `tracks` directory.  
- The silhouette is added to the subdirectory as `{animal-name}_silhouette.png`.  
- [POTrace](http://potrace.sourceforge.net/) is used to convert the silhouette to SVG.
- SVG is rendered to a new, high-quality bitmap.
- HQ bitmap is tweaked into an esimated height map.
- A normal map is generated using code adapted from [Mehdi-Antoine's Normal Map Generator](https://github.com/Mehdi-Antoine/NormalMapGenerator).


## Status
The table below will be updated as I finish each track.

|Animal               |Silhouette|SVG|HQ Bitmap|Displacement & Normals|
|---------------------|----------|---|---------|----------------------|
|Antelope             |<img src="./tracks/antelope/antelope_silhouette.png" height=30>|||
|Armadillo            |<img src="./tracks/armadillo/armadillo_silhouette.png" height=30>|||
|Badger               |<img src="./tracks/badger/badger_silhouette.png" height=30>|||
|Bear (Black) (Front) |<img src="./tracks/bear-black/bear-black_front_silhouette.png" height=30>|||
|Bear (Black) (Rear)  |<img src="./tracks/bear-black/bear-black_rear_silhouette.png" width=30>|||
|Bear (Brown) (Front) |<img src="./tracks/bear-brown/bear-brown_front_silhouette.png" width=30>|||
|Bear (Brown) (Rear)  |<img src="./tracks/bear-brown/bear-brown_rear_silhouette.png" width=30>|||
|Beaver               |<img src="./tracks/beaver/beaver_silhouette.png" height=30>|||
|Bison                |<img src="./tracks/bison/bison_silhouette.png" height=30>|||
|Bobcat               |<img src="./tracks/bobcat/bobcat_silhouette.png" height=30>|||
|Caribou              |<img src="./tracks/caribou/caribou_silhouette.png" height=30>|||
|Cat                  |<img src="./tracks/cat/cat_silhouette.png" height=30>|||
|Cougar (Front)       |<img src="./tracks/cougar/cougar_front_silhouette.png" height=30>|||
|Cougar (Rear)        |<img src="./tracks/cougar/cougar_rear_silhouette.png" width=30>|||
|Coyote               |<img src="./tracks/coyote/coyote_silhouette.png" height=30>|||
|Deer (Mule)          |<img src="./tracks/deer-mule/deer-mule_silhouette.png" height=30>|||
|Deer (Whitetail)     |<img src="./tracks/deer-whitetail/deer-whitetail_silhouette.png" height=30>|||
|Dog                  |<img src="./tracks/dog/dog_silhouette.png" height=30>|||
|Elk                  |<img src="./tracks/elk/elk_silhouette.png" height=30>|||
|Ferret               |<img src="./tracks/ferret/ferret_silhouette.png" height=30>|||
|Fisher               |<img src="./tracks/fisher/fisher_silhouette.png" height=30>|||
|Fox (Kit)            |<img src="./tracks/fox-kit/fox-kit_silhouette.png" height=30>|||
|Fox (Red)            |<img src="./tracks/fox-red/fox-red_silhouette.png" height=30>|||
|Jack Rabbit          |<img src="./tracks/jackrabbit/jackrabbit_silhouette.png" height=30>|||
|Lynx                 |<img src="./tracks/lynx/lynx_silhouette.png" height=30>|||
|Marmot               |<img src="./tracks/marmot/marmot_silhouette.png" height=30>|||
|Marten               |<img src="./tracks/marten/marten_silhouette.png" height=30>|||
|Mink                 |<img src="./tracks/mink/mink_silhouette.png" height=30>|||
|Moose                |<img src="./tracks/moose/moose_silhouette.png" height=30>|||
|Mountain Goat        |<img src="./tracks/goat-mountain/goat-mountain_silhouette.png" height=30>|||
|Mountain Sheep       |<img src="./tracks/sheep-mountain/sheep-mountain_silhouette.png" height=30>|||
|Muskox               |<img src="./tracks/muskox/muskox_silhouette.png" height=30>|||
|Muskrat              |<img src="./tracks/muskrat/muskrat_silhouette.png" height=30>|||
|Ocelot               |<img src="./tracks/ocelot/ocelot_silhouette.png" height=30>|||
|Opossum              |<img src="./tracks/opossum/opossum_silhouette.png" height=30>|||
|Otter                |<img src="./tracks/otter/otter_silhouette.png" height=30>|||
|Peccary              |<img src="./tracks/peccary/peccary_silhouette.png" height=30>|||
|Pheasant             |<img src="./tracks/pheasant/pheasant_silhouette.png" height=30>|||
|Pig                  |<img src="./tracks/pig/pig_silhouette.png" height=30>|||
|Porcupine            |<img src="./tracks/porcupine/porcupine_silhouette.png" height=30>|||
|Prairie Dog          |<img src="./tracks/prairie_dog/prairie_dog_silhouette.png" height=30>|||
|Raccoon (Front)      |<img src="./tracks/raccoon/raccoon_front_silhouette.png" height=30>|||
|Raccoon (Rear)       |<img src="./tracks/raccoon/raccoon_rear_silhouette.png" width=30>|||
|Skunk                |<img src="./tracks/skunk/skunk_silhouette.png" height=30>|||
|Squirrel (Gray)      |<img src="./tracks/squirrel-gray/squirrel-gray_silhouette.png" height=30>|||
|Turkey               |<img src="./tracks/turkey/turkey_silhouette.png" height=30>|||
|Wild Boar            |<img src="./tracks/boar-wild/boar-wild_silhouette.png" height=30>|||
|Wolf (Gray)          |<img src="./tracks/wolf-gray/wolf-gray_silhouette.png" height=30>|||
|Wolverine            |<img src="./tracks/wolverine/wolverine_silhouette.png" height=30>|||
|Woodchuck            |<img src="./tracks/woodchuck/woodchuck_silhouette.png" height=30>|||

### Sources
The original reference image is included with the repository, as well as a few cleaned up versions.  The original appears to be a scan from a book, and has been shared hundreds of times across the internet.  I can not find the original source, but if you know it I would appreciate being able to cite it here.

<img src="./references/tracks_transparency.png">

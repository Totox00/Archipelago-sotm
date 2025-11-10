rm ./custom_worlds/sotm.apworld
cd ./worlds
zip ../custom_worlds/sotm.apworld ./sotm/**
cd ./sotm
zip ../../custom_worlds/sotm.apworld ./archipelago.json

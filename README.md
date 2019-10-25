Would like to be able to use dataclasses structure. Its possible now but the type hinting is needed, and its not enforced so just seems bad to use.


make it so __repr__ is ambigious


Should have a function to register the config object in the anyfig module which can later simply be imported anywhere. Singleton idea. No more passing around configs

Name suggestions:
Anyfig


Do we want to let users be able to create several configs? The fire/argparse doesn't work then. Unless we hook into that and divides it... But not for v1

Mark classes / properties as final? For properties, it would be cool to just
do them as uppercase, which is python convention.
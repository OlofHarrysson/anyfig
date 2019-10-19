Can I simply decorate config class? Or also want/need to inherit?

Do I want to assert so that class name isnt same as MasterConfig?

Do I want to inherit dataclasses? Whats the benefit? Do I automatically get freeze, hash, eq etc?


Need to be able to load configs. How does it work with objects?


How do we print objects?
How do we print nested configs?
If we have a function, which then calls another function. Can we show source code for both?


Would like to be able to use dataclasses structure. Its possible now but the type hinting is needed, and its not enforced so just seems bad to use.


make it so __repr__ is ambigious


Should have a function to register the config object in the anyfig module which can later simply be imported anywhere. No more passing around configs

Name suggestions:
Anyfig



Do we want to let users be able to create several configs? The fire/argparse doesn't work then. Unless we hook into that and divides it... But not for v1
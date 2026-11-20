# Skenario C: Distributed Spatial Tiling & Resource Deadlock

Empat worker (`W1..W4`) bernavigasi dan mengunci sel di grid 3D `4×4×4`.
Invarian terkunci menjamin *mutual exclusion* dan bebas *circular wait* `>= 4` tick berturut-turut.

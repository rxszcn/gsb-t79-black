# flags: --minimum-version=3.12
def f(  # fmt: skip
    a, b
):
    pass


class C(  # fmt: skip
    Base
):
    pass


async def g(  # fmt: skip
    a
):
    pass


with (  # fmt: skip
    a as b,
):
    pass


if (  # fmt: skip
    a and b
):
    pass


for i in (  # fmt: skip
    a, b
):
    pass


while (  # fmt: skip
    a and b
):
    pass


from m import (  # fmt: skip
    a,
    b,
)


def h[*Ts](): pass  # fmt: skip


def i[**P](): pass  # fmt: skip


async def j():
    async with ctx(): print("a"); print("b")  # fmt: skip


async def k():
    async for i in x(): print(i); print("d")  # fmt: skip

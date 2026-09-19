# 在仓库根目录跑：PYTHONPATH=src .venv/bin/python repro/fmtskip-header.py
import black
from black import Mode, format_str

FREEZE_PROOF = [
    "if (\n    a ==    3\n    and b    != 9\n    and c is not None\n):  # fmt: skip\n    pass\n",
    "if (\n    a ==    3\n    and b    != 9  # fmt: skip\n    and c is not None\n):\n    pass\n",
]

HOLE = {
    "def": "def f(  # fmt: skip\n    a, b\n):\n    pass\n",
    "class": "class C(  # fmt: skip\n    Base\n):\n    pass\n",
    "async-def": "async def f(  # fmt: skip\n    a\n):\n    pass\n",
    "with": "with (  # fmt: skip\n    a as b,\n):\n    pass\n",
    "if": "if (  # fmt: skip\n    a and b\n):\n    pass\n",
    "for": "for i in (  # fmt: skip\n    a, b\n):\n    pass\n",
    "while": "while (  # fmt: skip\n    a and b\n):\n    pass\n",
    "import": "from m import (  # fmt: skip\n    a,\n    b,\n)\n",
    "typeparams": "def f[*Ts](): pass  # fmt: skip\n",
    "paramspec": "def f[**P](): pass  # fmt: skip\n",
    "async-with-oneline": 'async def g():\n    async with ctx(): print("a"); print("b")  # fmt: skip\n',
    "async-for-oneline": "async def g():\n    async for i in x(): print(i); print('d')  # fmt: skip\n",
}


def report(src):
    try:
        out = format_str(src, mode=Mode())
    except Exception as e:
        return "raised %s: %s" % (type(e).__name__, str(e).splitlines()[0][:70])
    marks = []
    try:
        black.assert_equivalent(src, out)
    except Exception as e:
        marks.append(type(e).__name__)
    try:
        black.assert_stable(src, out, mode=Mode())
    except Exception as e:
        marks.append("unstable:" + type(e).__name__)
    same = "unchanged" if out == src else "CHANGED"
    return "%s %s\n      out=%r" % (same, " ".join(marks), out)


print("=== 同一条注释，放在冒号行 / 放在中间行 ===")
for src in FREEZE_PROOF:
    print("  in : " + repr(src))
    print("  -> " + report(src))

print()
print("=== 注释放在以左括号结尾的那一行 ===")
for name, src in HOLE.items():
    print("  %-24s in=%r" % (name, src))
    print("  %-24s -> %s" % ("", report(src)))

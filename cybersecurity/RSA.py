# -*- coding: utf-8 -*-
# 网络安全实验二：RSA 算法的实现
# 运行环境：Python 3.9+，需要安装 gmpy2（pip install gmpy2）

import random
import time

import gmpy2
from gmpy2 import mpz

SEP = "=" * 64


def ask(prompt):
    """读取一行输入（直接回车使用默认值），并保证后续输出另起一行"""
    text = input(prompt).strip()
    print()
    return text


# ---------------------- 一、gmpy2 大素数生成 ----------------------

def gen_prime(bits, rs):
    """调用 gmpy2 生成一个 bits 位的随机大素数。

    思路：先用 mpz_urandomb 产生 bits 位随机整数，把最高位置 1 保证位数、
    最低位置 1 保证是奇数，再用 gmpy2.next_prime 求其后的素数。
    next_prime 内部先用小素数试除，再用 Miller-Rabin 做素性检验。
    """
    cand = mpz(gmpy2.mpz_urandomb(rs, bits))
    cand = cand | (mpz(1) << (bits - 1)) | mpz(1)   # 保证最高位、最低位为 1
    return mpz(gmpy2.next_prime(cand))


def gen_distinct_primes(bits, count, rs):
    """生成 count 个互不相同的大素数"""
    primes = []
    while len(primes) < count:
        p = gen_prime(bits, rs)
        if p not in primes:
            primes.append(p)
    return primes


# ---------------------- 二、扩展欧几里得算法求逆元 ----------------------

def ext_gcd(a, b):
    """扩展欧几里得算法：返回 (g, x, y)，满足 a*x + b*y = g = gcd(a, b)。

    用迭代的欧几里得除法 + 回代实现，避免递归过深。
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def mod_inverse(a, m):
    """用扩展欧几里得算法求 a 关于模 m 的逆元，即求 d 使 a*d ≡ 1 (mod m)"""
    a %= m
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        raise ValueError(f"{a} 与 {m} 不互素，逆元不存在")
    return x % m


# ---------------------- 三、模指数运算 ----------------------

def mod_exp_slow(x, b, m):
    """传统方法：连乘 b 次，共 b 次乘法和取模，复杂度 O(b)"""
    x %= m
    result = 1
    for _ in range(int(b)):
        result = result * x % m
    return result


def mod_exp_fast(x, b, m, verbose=False):
    """重复平方相乘法（快速模指数）：把指数写成二进制，复杂度 O(log b)

    b = sum(bit_i * 2^i)，于是 x^b = prod(x^(2^i))，只需反复平方再乘入结果。
    """
    b = int(b)
    x %= m
    result = 1
    if verbose:
        print(f"指数 b = {b}，二进制 b = {bin(b)[2:]}")
    i = 0
    while b > 0:
        if b & 1:
            result = result * x % m
            if verbose:
                print(f"  第 {i} 位为 1（权 2^{i}）：result = {result}")
        x = x * x % m
        b >>= 1
        i += 1
    return result


# ---------------------- 四、RSA 加解密 ----------------------

class RSA:
    def __init__(self, bits=512, e=65537, rs=None):
        self.bits = bits
        self.e = mpz(e)
        self.rs = rs if rs is not None else gmpy2.random_state(random.getrandbits(32))
        self.p = self.q = self.n = self.phi = self.d = None

    def generate_keys(self, verbose=False):
        """生成密钥对：p、q 各 bits/2 位，n = p*q，φ(n) = (p-1)(q-1)，d = e^(-1) mod φ"""
        half = self.bits // 2
        while True:
            p = gen_prime(half, self.rs)
            q = gen_prime(half, self.rs)
            n = p * q
            phi = (p - 1) * (q - 1)
            if (p != q and n.bit_length() == self.bits
                    and gmpy2.gcd(self.e, phi) == 1):
                break
        self.p, self.q, self.n, self.phi = p, q, n, phi
        self.d = mpz(mod_inverse(self.e, self.phi))
        if verbose:
            print(f"p = {int(self.p)}")
            print(f"q = {int(self.q)}")
            print(f"n = p*q = {int(self.n)}（{self.n.bit_length()} 比特）")
            print(f"φ(n) = (p-1)(q-1) = {int(self.phi)}")
            print(f"公钥 (n, e) = ({int(self.n)}, {int(self.e)})")
            print(f"私钥 d = {int(self.d)}")
        return self.n, self.e, self.d

    def encrypt(self, m):
        """加密：c = m^e mod n（快速模指数）"""
        return mpz(mod_exp_fast(m, self.e, self.n))

    def decrypt(self, c):
        """解密：m = c^d mod n（快速模指数）"""
        return mpz(mod_exp_fast(c, self.d, self.n))


def text_to_int(text):
    """字符串按 UTF-8 编码转成大整数"""
    return mpz(int.from_bytes(text.encode("utf-8"), "big"))


def int_to_text(num):
    """大整数按 UTF-8 解码回字符串"""
    length = (int(num).bit_length() + 7) // 8
    return int(num).to_bytes(length, "big").decode("utf-8", errors="ignore")


# ---------------------- 五、正确性检验 ----------------------

def check_big_mul(a, b, mods=(1000003, 2147483647, 999999937)):
    """检验两个大数相乘的结果是否正确。

    1) 交叉验证：Python 内置 int 乘法（Karatsuba）与 gmpy2.mul（GMP）各算一遍，
       两种独立实现结果相同才可信；
    2) 取模校验：任取模数 r，都应有 (a*b) mod r == ((a mod r)*(b mod r)) mod r，
       只要有一条不成立就说明乘法结果有错。
    """
    prod_py = int(a) * int(b)
    prod_gmp = int(gmpy2.mul(mpz(a), mpz(b)))
    print(f"Python 内置乘法结果：{str(prod_py)[:24]}...（共 {len(str(prod_py))} 位十进制）")
    print(f"gmpy2  乘法结果    ：{str(prod_gmp)[:24]}...（共 {len(str(prod_gmp))} 位十进制）")
    ok = prod_py == prod_gmp
    print(f"两种独立实现结果一致：{ok}")
    for r in mods:
        left = prod_py % r
        right = (int(a) % r) * (int(b) % r) % r
        flag = left == right
        ok = ok and flag
        print(f"  模 r={r:<10}：乘积余数 = {left:<10}，两因子余数之积 = {right:<10}，一致：{flag}")
    return ok


def verify_rsa(rsa, m):
    """用三种互相独立的方式检验 RSA 程序是否正确"""
    c = rsa.encrypt(m)
    m2 = rsa.decrypt(c)
    print("检验 1：解密结果是否还原明文")
    print(f"  明文 m  = {int(m)}")
    print(f"  解密 m' = {int(m2)}")
    print(f"  m' == m：{m2 == m}")

    print("检验 2：与标准实现交叉验证模指数")
    c_py = pow(int(m), int(rsa.e), int(rsa.n))
    c_gmp = int(gmpy2.powmod(mpz(m), rsa.e, rsa.n))
    print(f"  本程序加密 c = {int(c)}")
    print(f"  pow() 结果  = {c_py}")
    print(f"  gmpy2.powmod 结果 = {c_gmp}")
    same = (int(c) == c_py == c_gmp)
    print(f"  三者一致：{same}")

    print("检验 3：密钥关系 e*d ≡ 1 (mod φ(n))")
    check = int(rsa.e) * int(rsa.d) % int(rsa.phi)
    print(f"  e*d mod φ(n) = {check}（应为 1）")
    return m2 == m and same and check == 1


# ---------------------- 主程序 ----------------------

if __name__ == "__main__":
    seed_text = ask("请输入随机种子（直接回车使用默认值 20261030，同一 seed 结果可复现）：")
    seed = int(seed_text) if seed_text else 20261030
    rs = gmpy2.random_state(seed)

    print(SEP)
    print("1. 调用 gmpy2 生成不同大小的大素数")
    print(SEP)
    for bits in (16, 32, 64, 128, 256, 512):
        t0 = time.perf_counter()
        p = gen_prime(bits, rs)
        cost = (time.perf_counter() - t0) * 1e6
        print(f"{bits:>4} 位素数（十进制 {len(str(int(p)))} 位，耗时 {cost:.1f} us）：")
        print(f"     {int(p)}")
        print(f"     gmpy2.is_prime 复检：{gmpy2.is_prime(p)}")
    print("\n同一位数连续生成 3 个互不相同的素数：")
    for p in gen_distinct_primes(64, 3, rs):
        print(f"     {int(p)}")

    print("\n" + SEP)
    print("2. 扩展欧几里得算法求模逆元")
    print(SEP)
    a, m = 3674911, 6007800
    g, x, y = ext_gcd(a, m)
    print(f"ext_gcd({a}, {m}) = (g={g}, x={x}, y={y})")
    print(f"验证 {a}*({x}) + {m}*({y}) = {a * x + m * y}")
    d = mod_inverse(a, m)
    print(f"{a} 关于模 {m} 的逆元 d = {d}")
    print(f"验证 {a}*{d} mod {m} = {a * d % m}")
    print(f"与 gmpy2.invert 对比：{int(gmpy2.invert(mpz(a), mpz(m)))}"
          f"（一致：{d == int(gmpy2.invert(mpz(a), mpz(m)))}）")

    print("\n" + SEP)
    print("3. 模指数运算：传统方法与重复平方相乘法")
    print(SEP)
    print("例 1：小指数演示（b = 35，二进制 100011）")
    print("重复平方相乘法的计算过程：")
    r_fast = mod_exp_fast(3, 35, 1000000007, verbose=True)
    print(f"快速算法结果：3^35 mod 1000000007 = {r_fast}")
    print(f"传统方法结果：3^35 mod 1000000007 = {mod_exp_slow(3, 35, 1000000007)}")
    print(f"Python 内置 pow：{pow(3, 35, 1000000007)}")

    x, b, mod = 5234673, 3674911, 6012707
    print(f"\n例 2：x = {x}（< 10^9），b = {b}，m = {mod}")
    t0 = time.perf_counter()
    slow = mod_exp_slow(x, b, mod)
    t_slow = time.perf_counter() - t0
    t0 = time.perf_counter()
    fast = mod_exp_fast(x, b, mod)
    t_fast = time.perf_counter() - t0
    print(f"传统方法（连乘 {b} 次）：{slow}，耗时 {t_slow * 1e3:.2f} ms")
    print(f"快速方法（重复平方相乘）：{fast}，耗时 {t_fast * 1e6:.1f} us")
    print(f"结果一致：{slow == fast}，快速方法是传统方法速度的约 {t_slow / t_fast:.0f} 倍")

    print("\n" + SEP)
    print("4. 用实验大纲给出的数据检验 RSA 程序")
    print(SEP)
    p0, q0, e0, m0, c0 = 2357, 2551, 3674911, 5234673, 3650502
    n0 = p0 * q0
    phi0 = (p0 - 1) * (q0 - 1)
    d0 = mod_inverse(e0, phi0)
    print(f"p = {p0}, q = {q0}, n = p*q = {n0}, φ(n) = {phi0}")
    print(f"e = {e0}, d = {d0}（期望 422191，一致：{d0 == 422191}）")
    c_calc = mod_exp_fast(m0, e0, n0)
    m_calc = mod_exp_fast(c0, d0, n0)
    m_calc2 = mod_exp_fast(c_calc, d0, n0)
    print(f"加密 m = {m0}：c = m^e mod n = {c_calc}（期望 {c0}，一致：{c_calc == c0}）")
    print(f"解密 c = {c0}：m = c^d mod n = {m_calc}（期望 {m0}，一致：{m_calc == m0}）")
    print(f"自加密自解密：{m_calc2}（一致：{m_calc2 == m0}）")

    print("\n" + SEP)
    print("5. RSA 加解密演示（随机大素数）")
    print(SEP)
    bits_text = ask("请输入密钥位数（直接回车使用默认值 512）：")
    bits = int(bits_text) if bits_text else 512
    rsa = RSA(bits=bits, e=65537, rs=rs)
    t0 = time.perf_counter()
    rsa.generate_keys(verbose=True)
    print(f"密钥生成耗时：{(time.perf_counter() - t0) * 1e3:.2f} ms")

    msg = ask("请输入明文（直接回车使用默认值：陕西师范大学网络安全）：") or "陕西师范大学网络安全"
    m = text_to_int(msg)
    if m >= rsa.n:
        print("明文过长（消息对应的整数必须小于 n），请缩短明文后重试")
        m = mpz(123456789)          # 后续检验改用一个小明文
        print(f"后面的检验改用小明文 m = {int(m)}")
    else:
        print(f"\n明文：{msg}（UTF-8 编码转整数 m = {int(m)}）")
        c = rsa.encrypt(m)
        print(f"密文：c = m^e mod n = {int(c)}")
        m2 = rsa.decrypt(c)
        print(f"解密：m' = c^d mod n = {int(m2)}")
        print(f"还原明文：{int_to_text(m2)}")
        print(f"解密正确：{m2 == m}")

        print("\n快速模指数与传统模指数在 512 位密钥下的对比：")
        print(f"  私钥 d 的二进制长度：{int(rsa.d).bit_length()} 位")
        print(f"  快速模指数只需约 {2 * int(rsa.d).bit_length()} 次模乘")
        print(f"  传统方法需要 {int(rsa.d)} 次模乘，按每秒 10^7 次估算约需 "
              f"{float(mpz(int(rsa.d)) / mpz(10) ** 7 / mpz(31557600)):.3e} 年，实际不可行")

    print("\n" + SEP)
    print("6. 程序正确性检验")
    print(SEP)
    print("(1) 大数乘法的检验（两个 256 位随机整数的乘积）")
    a_big = mpz(gmpy2.mpz_urandomb(rs, 256))
    b_big = mpz(gmpy2.mpz_urandomb(rs, 256))
    print(f"a = {int(a_big)}")
    print(f"b = {int(b_big)}")
    mul_ok = check_big_mul(a_big, b_big)

    print("\n(2) RSA 加解密的三项检验")
    rsa_ok = verify_rsa(rsa, m) if m < rsa.n else False

    print("\n(3) 用随机明文批量测试")
    all_ok = True
    for _ in range(5):
        rnd = mpz(gmpy2.mpz_urandomb(rs, rsa.n.bit_length() - 1))
        if rsa.decrypt(rsa.encrypt(rnd)) != rnd:
            all_ok = False
    print(f"5 组随机明文加解密全部还原：{all_ok}")

    print(f"\n结论：大数乘法检验 {'通过' if mul_ok else '失败'}，"
          f"RSA 检验 {'通过' if rsa_ok else '失败'}，"
          f"随机测试 {'通过' if all_ok else '失败'}")

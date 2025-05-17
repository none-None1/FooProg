#include<fstream>
#include<iostream>
#include "fp.hpp"
unsigned char qq[1000000];
using namespace std;
map<ull, foo_t> m;
int q;
ull tob(int i) {
        ull res = 0,n=1;
        for (int j = i; j < i + 8; j++) {
                res += qq[j] * n;
                n <<= 8;
        }
        return res;
}
int inline newstrlen(const char* x) {
        int i = 0;
        for (; x[i]; i++);
        return i;
}
foo_t inline mget(ull addr) {
        return m.lower_bound(addr)->second;
}
void inline mset(ull addr, foo_t val) {
        m[addr] = val;
}
void _instruction_00() {
        ull a = tob(q + 1), b = tob(q + 9), c = tob(q + 17);
        foo_t x = mget(a), y = mget(b);
        foo_t z = x + y;
        mset(c, z);
        q += 25;
}
void _instruction_01() {
        ull a = tob(q + 1), b = tob(q + 9), c = tob(q + 17);
        foo_t x = mget(a), y = mget(b);
        foo_t z = x - y;
        mset(c, z);
        q += 25;
}
void _instruction_02() {
        ull a = tob(q + 1), b = tob(q + 9), c = tob(q + 17);
        foo_t x = mget(a), y = mget(b);
        foo_t z = x * y;
        mset(c, z);
        q += 25;
}
void _instruction_03() {
        ull a = tob(q + 1), b = tob(q + 9), c = tob(q + 17);
        foo_t x = mget(a), y = mget(b);
        foo_t z = x / y;
        mset(c, z);
        q += 25;
}
void _instruction_04() {
        ull a = tob(q + 1);
        unsigned char b = qq[q + 9];
        if (b == 1) {
                double c = atof((const char *)(qq + q + 10));
                m[a] = c;
                int y = newstrlen((const char *)(qq + q + 10));
                q += 11 + y;
        }
        else {
                m[a] = tob(q + 10);
                q += 18;
        }
}
void _instruction_05() {
        ull a = tob(q + 1), b = tob(q + 9);
        mset(a, mget(b));
        q += 17;
}
void _instruction_06() {
        ull a = tob(q + 1);
        foo_t f;
        cin >> f;
        mset(a, f);
        q += 9;
}
void _instruction_07() {
        ull a = tob(q + 1);
        cout << mget(a) << endl;
        q += 9;
}
void _instruction_08() {
        ull a = tob(q + 1), b = tob(q + 9);
        if (bool(mget(a))) q = b;
        else q += 17;
}
void * functions[] = { _instruction_00,_instruction_01 ,_instruction_02 ,_instruction_03 ,_instruction_04 ,_instruction_05 ,_instruction_06 ,_instruction_07 ,_instruction_08 };
int main(int argc, char* argv[]) {
        if (argc < 2) {
                cerr << "FooProg binary interpreter needs at least 1 argument" << endl;
                return 0;
        }
        ifstream fi(argv[1],ios::binary);
        if (!fi) {
                cerr << "Cannot open file " << argv[1];
                return -1;
        }
        int p = 0;
        while (!fi.eof()) {
                fi.read((char *)(qq + (p++)), 1);
        }
        p--;
        q = 0;
        while (q < p) {
                ((void(*)())functions[qq[q]])();
        }

        return 0;
}
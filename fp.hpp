#pragma once
#include<fstream>
#include<iostream>
#include<map>
#include<algorithm>
#include<cstdlib>
#include<cstring>
#define ll long long
#define ull unsigned long long
using namespace std;
struct foo_t {
        ull l;
        double d;
        int t;
        foo_t() {
                l = 0;
                d = 0;
                t = 0;
        }
        void operator=(ull x) {
                if (t == 2) d = x;
                else t = 1,l = x;
        }
        void operator=(double x) {
                if (t == 2) d = x;
                else {
                        t = 2;
                        d = x;
                }
        }
        foo_t operator+(foo_t b) {
                foo_t c = *this;
                int t2 = max(c.t, b.t);
                if (t2 == 1) {
                        c.l = c.l + b.l;
                        c.t = 1;
                }
                else {
                        double d2 = 0;
                        if (c.t == 1) d2 += c.l;
                        else d2 += c.d;
                        if (b.t == 1) d2 += b.l;
                        else d2 += b.d;
                        c.d = d2;
                        c.t = 2;
                }
                return c;
        }
        foo_t operator-(foo_t b) {
                foo_t c = *this;
                int t2 = max(c.t, b.t);
                if (t2 == 1) {
                        c.l = c.l - b.l;
                        c.t = 1;
                }
                else {
                        double d2 = 0;
                        if (c.t == 1) d2 += c.l;
                        else d2 += c.d;
                        if (b.t == 1) d2 -= b.l;
                        else d2 -= b.d;
                        c.d = d2;
                        c.t = 2;
                }
                return c;
        }
        foo_t operator*(foo_t b) {
                foo_t c = *this;
                int t2 = max(c.t, b.t);
                if (t2 == 1) {
                        c.l = c.l * b.l;
                        c.t = 1;
                }
                else {
                        double d2 = 1;
                        if (c.t == 1) d2 *= c.l;
                        else d2 *= c.d;
                        if (b.t == 1) d2 *= b.l;
                        else d2 *= b.d;
                        c.d = d2;
                        c.t = 2;
                }
                return c;
        }
        foo_t operator/(foo_t b) {
                foo_t c = *this;
                int t2 = max(c.t, b.t);
                if (t2 == 1) {
                        c.l = c.l / b.l;
                        c.t = 1;
                }
                else {
                        double d2 = 1;
                        if (c.t == 1) d2 *= c.l;
                        else d2 *= c.d;
                        if (b.t == 1) d2 /= b.l;
                        else d2 /= b.d;
                        c.d = d2;
                        c.t = 2;
                }
                return c;
        }
        operator bool() {
                if (t == 1) return bool(l);
                else return bool(d);
        }
        friend ostream& operator<<(ostream& o, foo_t f);
        friend istream& operator>>(istream& i, foo_t& f);
};
ostream& operator<<(ostream& o, foo_t f) {
        if (f.t == 1) o << f.l;
        else o << f.d;
        return o;
}
istream& operator>>(istream& i, foo_t& f) {
        double d;
        i >> d;
        f.d = d;
        return i;
}
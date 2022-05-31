---
layout: post
title:  "Binary Search 1"
date:   2022-05-31 17:37:14 +0530
categories: codeforces
---

<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
		tex2jax: {
			inlineMath: [['$', '$']]
		}
	});
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

Binary Search applies to many problems on Codeforces. These problems can be framed as -- find the largest $x \in [n]$ for which $f(x)$ is true. If $f$ has the monotonicity property:

$$
f(x) \Rightarrow f(x - 1)
$$

Then we can _binary search_ for the largest $x$. This helps when evaluating $f$ on each $x$ is prohibitively expensive. When monotonicity holds, we can guess $O(lg n)$ $x$'s and evaluate $f$ on just those to find the largest.

## [Keshi Is Throwing a Party](https://codeforces.com/contest/1610/problem/C)

This is an example where Binary Search yields a simple and efficient solution. In a nutshell, we are given $[n]$ and two arrays $a_1 \cdots a_n$, $b_1 \cdots b_n$. We have to find the largest set $S \subseteq [n]$ that satisfies -- for all $i \in S$, there are at most $a_i$ elements in $S$ which are greater than $i$ and at most $b_i$ elements in $S$ which are lesser than $i$. 

For example: 

```python
# assume for now that arrays are 1-indexed
n = 3
a = [1, 2, 1]
b = [2, 1, 1]
```

Then $S = \\{1, 2\\}$ is a _valid_ subset.

The key to solving this problem is that the question -- does a _valid_ set of size $x$ exists? -- has the monotonicity property. If a _valid_ set of size $x$ exists, simply remove the last element and obtain a _valid_ set of size $x - 1$. 

```python
# returns true if a valid set of size x exists
# def checker (x) : 
#   ...
l, r = 1, n 
while l < r : 
  m = (l + r) / 2
  if checker(m + 1) : 
    l = m + 1
  else :
    r = m

print(l) 
```

Finally, we can write `checker` using a simple greedy strategy. We build the set $S$ by scanning through $1 \cdots n$ and greedily adding the first $i$ to $S$ that satisfies $\|S\| \leq b_i$ and $x - (\|S\| + 1) \leq a_i$. If at the end of the scan, $\|S\| < x$, we report that that a size $x$ _valid_ set doesn't exist. 

Why does `checker` correct? If `checker` is incorrect, that means that for some $x$, there is a _valid_ $S$ of that size $x$ but `checker` only finds $S'$ and $\|S'\| = k < x$. 

$$
S = \{i_1, \cdots, i_x\}
$$

$$
S' = \{j_1, \cdots, j_k\}
$$

Let $l$ be the smallest index where $S$ and $S'$ differ. There has to be some $l \in [k]$ for which $i_l \neq j_l$ because otherwise `checker` would have extended $S'$. Since `checker` picks the earliest item to add to the set: $j_l < i_l$. Both $j_l$ and $i_l$ satisfy the _validity_ condition. 

$$
l - 1 \leq b[j_l] 
$$

$$
l - 1 \leq b[i_l] 
$$

$$
x - l \leq a[j_l] 
$$

$$
x - l \leq a[i_l] 
$$

Hence we can replace $i_l \in S$ by $j_l$. The new set $S^{(1)} = S - \\{i_l\\} + \\{j_l\\}$ is still _valid_. Repeating this process $k - l + 1$ times gives us $S^{(k - l + 1)}$ for which no $l \in [k]$ exists where $S^{(k - l + 1)}$ and $S'$ differ. But such an $l$ _has_ to exist and so we reach a contradiction, proving that `checker` is correct.

I'll end the story here. [Here](https://codeforces.com/contest/1610/submission/136793593) is my submission on Codeforces. In summary, under certain conditions, Binary Search allows us to convert an optimization problem (_find the largest x for which ..._) into a decision problem (_does there exist an x for which ..._). When applicable, Binary Search introduces only a small multiplicative $O(lg n)$ overhead over the underlying decision problem.

I'm slightly disappointed that I haven't been able to find an efficient dynamic-programming solution to this problem. If anyone knows of one, please tell me!

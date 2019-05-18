from typing import List
import time

gamma = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

freq = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015,
        6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929,
        0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

esGamma = ['a', 'b', 'c', 'd']
esP = [0.9, 0.05, 0.025, 0.025]


p_freq = []

for x in freq:
    p_freq.append(x/100.0)


class Node:
    def __init__(self, symbol, prob, left=None, right=None, parent=None, code=''):
        self.symbol = symbol
        self.prob = prob
        self.left = left
        self.right = right
        self.parent = parent
        self.code = code

    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.code + self.symbol
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.code + self.symbol
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.code + self.symbol
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.code + self.symbol
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def init_tree(symbols, freqs):
    nodes: List[Node] = []
    for i in range(0, len(symbols)):
        nodes.append(Node(symbols[i], freqs[i]))
    return nodes


def create_node(nodes):
    tempNode1 = Node(None, 1)
    for node in nodes:
        if node.prob < tempNode1.prob:
            tempNode1 = node
    nodes.remove(tempNode1)
    tempNode2 = Node(None, 1)
    for node in nodes:
        if node.prob < tempNode2.prob:
            tempNode2 = node
    nodes.remove(tempNode2)
    if len(tempNode1.symbol) <= len(tempNode2.symbol):
        result = Node(tempNode1.symbol+tempNode2.symbol, tempNode1.prob+tempNode2.prob, tempNode1, tempNode2)
    else:
        result = Node(tempNode2.symbol + tempNode1.symbol, tempNode1.prob + tempNode2.prob, tempNode2, tempNode1)
    tempNode2.parent = result
    tempNode1.parent = result
    nodes.append(result)
    return nodes


def build_tree(symbols, freq):
    nodes = init_tree(symbols, freq)
    while len(nodes) > 1:
        nodes = create_node(nodes)
    return nodes[0]


def assign_code(root):
    result = dict()
    if root.left is not None:
        root.left.code = root.code+'0'
        result.update(assign_code(root.left))
    else:
        return {root.symbol: root.code}
    if root.right is not None:
        root.right.code = root.code+'1'
        result.update(assign_code(root.right))
    else:
        return {root.symbol: root.code}
    return result


def assign_decode(code):
    decode_dict = dict()
    for c in code:
        decode_dict[code[c]] = c
    return decode_dict


def translate(code_dict):
    return lambda x: code_dict[x]


def encode(code_dict, text):
    result = ""
    for c in text:
        result += translate(code_dict)(c)
    return result


def decode(decode_dict, text):
    temp = ""
    result = ""
    for c in text:
        temp += c
        try:
            result += translate(decode_dict)(temp)
            temp = ""
        except KeyError:
            continue
    return result


r = build_tree(gamma, p_freq)
code_dict = assign_code(r)
decode_dict = assign_decode(code_dict)

e = encode(code_dict, "comeebellalaconigliachefaillattedivaniglia")
print(e)
d = decode(decode_dict, e)
print(d)

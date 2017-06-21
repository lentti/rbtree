class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.p=None
        self.color = None

        self.next=None # define a new property to make a Node-Stack

    def __str__(self):
        return str(self.key)


class NodeStk:
    def __init__(self): # initializing a Node-Stack
        self.head=Node(None)

    def is_empty(self): # check current stack is empty or not
        return self.head.next==None

    def push(self,node): # push a new node to stck  
        current = self.head
        while current.next:
            current=current.next # find last element
        current.next=node # last element.next = new Node

    def pop(self): # pop a node from stack
        if self.is_empty():
            return Node(None)
        prev=None # to delete a last node from stack, we define next to last element.next=None
        current = self.head
        while current.next: 
            prev=current # in this way we can find a element next to last
            current=current.next
        prev.next=None
        return current # return last element


    def print(self): # just to check I made right stack we don't usually use it
        if self.is_empty():
            print('Empty stack')
            return
        current=self.head.next
        while current.next:
            print(current.key)
            current=current.next
        print(current.key)


class RBT:
    def __init__(self):
        self.nil=Node(key=None)
        self.root=self.nil
        self.nil.color='b'

    def __len__(self):  return self.nil.color
    def __contains__(self,item):    return self.search(item) is not self.nil

    def insert(self,key):
        tempnode=Node(key)
        tempnode.left=self.nil
        tempnode.right=self.nil
        self.insert_node(tempnode)

    def insert_node(self,z):
        y=self.nil
        x=self.root
        while x != self.nil:
            y=x
            if z.key < x.key:
                x=x.left
            else:
                x=x.right
        z.p=y
        if y==self.nil:
            self.root=z
        elif z.key < y.key:
            y.left=z
        else:
            y.right=z
        z.left=self.nil
        z.right=self.nil
        z.color='r'
        self.insert_fix(z)

    def print(self,tree=None,level=None):
        if tree is None:
            tree=self.root
        if level is None:
            level=0
        if tree.right is not self.nil:
            self.print(tree.right,level + 1)
        for i in range(level):
            print('\t', end='')
        print(tree.key,end='')
        print(tree.color,str(level))
        if tree.left is not self.nil:
            self.print(tree.left, level + 1)


    def insert_fix(self,z):
        while z.p.color == 'r':
            if z.p == z.p.p.left:
                y=z.p.p.right
                if y.color == 'r':
                    z.p.color='b'
                    y.color='b'
                    z.p.p.color='r'
                    z=z.p.p
                else:
                    if z==z.p.right:
                        z=z.p
                        self.rotate(z,'l')
                    z.p.color='b'
                    z.p.p.color='r'
                    self.rotate(z.p.p,'r')
            else:
                y=z.p.p.left
                if y.color == 'r':
                    z.p.color='b'
                    y.color='b'
                    z.p.p.color='r'
                    z=z.p.p
                else:
                    if z==z.p.left:
                        z=z.p
                        self.rotate(z,'r')
                    z.p.color='b'
                    z.p.p.color='r'
                    self.rotate(z.p.p,'l')
        self.root.color='b'

    def rotate(self,x,rotation):
        if rotation == 'l':
            y=x.right
            x.right=y.left
            if y.left != self.nil:
                y.left.p=x
            y.p=x.p
            if x.p==self.nil:
                self.root =y
            elif x==x.p.left:
                x.p.left=y
            else:
                x.p.right=y
            y.left=x
            x.p=y
        if rotation == 'r':
            y=x.left
            x.left=y.right
            if y.right != self.nil:
                y.right.p=x
            y.p=x.p
            if x.p==self.nil:
                self.root =y
            elif x==x.p.right:
                x.p.right=y
            else:
                x.p.left=y
            y.right=x
            x.p=y


    def transplant(self,u,v):
        if u.p == self.nil:
            self.root = v
        elif u==u.p.left:
            u.p.left = v
        else:
            u.p.right=v
        v.p=u.p

    def search(self, key, x = None):
        if None is x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def searchWithParent(self, key, x = None):
        if None is x:
            x = self.root
        y=x
        while x != self.nil and key != x.key:
            if key < x.key:
                y=x
                x = x.left
            else:
                y=x
                x = x.right
        return x,y

    def successor(self,x):
        if x.right is not self.nil:
            return self.minimum(x.right)
        y=x.p
        while y is not self.nil and x is y.right:
            x=y
            y=y.p
        return y

    def predecessor(self,x):
        if x.left is not self.nil:
            return self.maximum(x.left)
        y=x.p
        while y is not self.nil and x is y.left:
            x=y
            y=y.p
        return y

    def minimum(self, x=None):
        if None is x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x

    def maximum(self, x=None):
        if None is x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def delete(self,z):
        self.deleteNode(self.search(z))
        
    def deleteNode(self,z):
        y=z
        yorigcolor=y.color
        if z.left == self.nil:
            x=z.right
            self.transplant(z,z.right)
        elif z.right==self.nil:
            x=z.left
            self.transplant(z,z.left)
        else:
            y=self.minimum(z.right)
            yorigcolor=y.color
            x=y.right
            if y.p ==z:
                x.p=y
            else:
                self.transplant(y,y.right)
                y.right=z.right
                y.right.p=y
            self.transplant(z,y)
            y.left=z.left
            y.left.p=y
            y.color=z.color
        if yorigcolor == 'b':
            self.delete_fix(x)
            
    def delete_fix(self,x):
        while x != self.root and x.color == 'b':
            if x==x.p.left:
                w=x.p.right
                if w.color =='r':
                    w.color='b'
                    x.p.color='r'
                    self.rotate(x.p,'l')
                    w=x.p.right
                if w.left.color is 'b' and w.right.color is 'b':
                    w.color = 'r'
                    x=x.p
                else:
                    if w.right.color =='b':
                        w.left.color ='b'
                        w.color='r'
                        self.rotate(w,'r')
                        w=x.p.right
                    w.color=x.p.color
                    x.p.color='b'
                    w.right.color ='b'
                    self.rotate(x.p,'l')
                    x=self.root
            else:
                w=x.p.left
                if w.color =='r':
                    w.color='b'
                    x.p.color='r'
                    self.rotate(x.p,'r')
                    w=x.p.left
                if w.left.color is 'b' and w.right.color is 'b':
                    w.color = 'r'
                    x=x.p
                else:
                    if w.left.color =='b':
                        w.right.color ='b'
                        w.color='r'
                        self.rotate(w,'l')
                        w=x.p.left
                    w.color=x.p.color
                    x.p.color='b'
                    w.left.color ='b'
                    self.rotate(x.p,'r')
                    x=self.root
        x.color ='b'


    def __len__(self):  return self.get_total()

    def get_total(self,tree=None):
        if tree is None:
            tree=self.root
        stk=NodeStk()
        cnt=0
        while stk.is_empty()==False or tree != self.nil: # loop until stack is empty and 
            if tree != self.nil:
                stk.push(tree)
                tree=tree.left
            else:
                tree=stk.pop()
                cnt+=1
                tree=tree.right
        return cnt

    def inorder_iter(self,tree=None): # a new method to traverse inorder in iteration
        if tree is None:
            tree=self.root
        stk=NodeStk()
        while stk.is_empty()==False or tree != self.nil: # loop until stack is empty and 
            if tree != self.nil:
                stk.push(tree)
                tree=tree.left
            else:
                tree=stk.pop()
                print(tree.key, tree.color.upper())
                tree=tree.right
        print('')

    def get_nb(self,tree=None):
        if tree is None:
            tree=self.root
        stk=NodeStk()
        cnt=0
        while stk.is_empty()==False or tree != self.nil: # loop until stack is empty and 
            if tree != self.nil:
                stk.push(tree)
                tree=tree.left
            else:
                tree=stk.pop()
                if tree.color is 'b':
                    cnt+=1
                tree=tree.right
        return cnt

    def get_bh(self,tree=None):
        if tree is None:
            tree=self.root
        cnt=0
        while tree is not self.nil:
            if tree.color is 'b':
                cnt+=1
            tree=tree.right
        return cnt

def readFile( filename ):
    with open(filename,'r') as f:
        lines = f.readlines()
    return lines

def readInputFile ( filename ):
    lines = readFile(filename)
    rbt=RBT()
    for line in lines:
        number=int(line)
        if number > 0:
            rbt.insert(number)
        elif number < 0:
            number*=-1
            if number in rbt:
                rbt.delete(number)
        elif number ==0:
            break
    return rbt

def printValue(a,b,c,f):
    if a.key is None:
        a='NIL'
    f.write(str(a)+' ')
    if b.key is None:
        b='NIL'
    f.write(str(b)+' ')
    if c.key is None:
        c='NIL'
    f.write(str(c)+'\n')

def printResult( rbt, number ,f):
    node,nodeParent=rbt.searchWithParent(number)
    if node != rbt.nil:
        printValue(rbt.predecessor(node), node, rbt.successor(node),f)
    else:
        if nodeParent.key < number:
            printValue(nodeParent,node,rbt.successor(nodeParent),f)
        else:
            printValue(rbt.predecessor(nodeParent),node,nodeParent,f)

def readSearchFile( rbt, filename ):
    f=open('output.txt','w');
    lines = readFile(filename)
    for line in lines:
        number=int(line)
        if number == 0:
            break
        printResult(rbt, number,f)
    f.close()


def main():
    rbt=readInputFile('input.txt')
    readSearchFile(rbt,'search.txt')

    
if __name__ == '__main__':
    main()

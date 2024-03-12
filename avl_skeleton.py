

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    @ complexity: O(1)
    """

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    """returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
    @ complexity: O(1)
	"""

    def getLeft(self):
        return self.left

    """returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
    @ complexity: O(1)
	"""

    def getRight(self):
        return self.right

    """returns the parent

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
    @ complexity: O(1)
	"""

    def getParent(self):
        return self.parent

    """return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
    @ complexity: O(1)
	"""

    def getValue(self):
        return self.value

    """returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
    @ complexity: O(1)
	"""

    def getHeight(self):
        return self.height

    """returns the size

	@rtype: int
	@returns: the size of self, 0 if the node is virtual
    @ complexity: O(1)
	"""

    def getSize(self):
        return self.size

    """returns the balnce factor

    @pre: self is a real node
	@rtype: int
	@returns: the balance factor of self
    @ complexity: O(1)
	"""

    def getBf(self):
        return self.left.getHeight() - self.right.getHeight()

    """sets left child

	@type node: AVLNode
	@param node: a node
    @ complexity: O(1)
	"""

    def setLeft(self, node):
        self.left = node

    """sets right child

	@type node: AVLNode
	@param node: a node
    @complexity: O(1)
	"""

    def setRight(self, node):
        self.right = node

    """ sets right child and also sets right child's parent
        @type child: AVLnode
        @param child: a node
        @complexity: O(1)
     """

    def completeSetRight(self, child):
        self.setRight(child)
        child.setParent(self)

    """ sets left child and also sets left child's parent
        @type child: AVLnode
        @param child: a node
        @complexity: O(1)
     """

    def completeSetLeft(self, child):
        self.setLeft(child)
        child.setParent(self)

    """sets parent

	@type node: AVLNode
	@param node: a node
    @complexity: O(1)
	"""

    def setParent(self, node):
        self.parent = node

    """sets value

	@type value: str
	@param value: data
    @complexity: O(1)
	"""

    def setValue(self, value):
        self.value = value

    """sets the height of the node

	@type h: int
	@param h: the height
    @complexity: O(1)
	"""

    def setHeight(self, h):
        self.height = h

    """sets the size of the node

	@type size: int
	@param size: the size
    @complexity: O(1)
	"""

    def setSize(self, size):  # Guy added this method
        self.size = size

    """
    updates node height by computing it from childrens' height 
    
    @complexity: O(1)
    """

    def updateHeight(self):
        self.setHeight(max(self.getRight().getHeight(),
                           self.getLeft().getHeight()) + 1)

    """
    updates node size by computing it from childrens' size

    @complexity: O(1)
    """

    def updateSize(self):
        self.setSize(self.getRight().getSize() + self.getLeft().getSize() + 1)

    """returns whether self is not a virtual node

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
    @complexity: O(1)
	"""

    def isRealNode(self):
        if self.height == -1:
            return False
        return True


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):

    """
    Constructor, you are allowed to add more fields.

    Initializing the fields root, first and last to None
    @complexity: O(1)
    """

    def __init__(self):
        self.root = None
        self.firstItem = None
        self.lastItem = None

    """returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
    @complexity: O(1)
	"""

    def empty(self):
        if self.root == None:
            return True
        return False

    """retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the value of the i'th item in the list.
                unless i is not a legal index on this list, then the return value would be None
    @complexity: O(log(i))
	"""

    def retrieve(self, i):
        if i < 0 or i >= self.length():
            return None
        else:
            return self.treeSelect(i+1).getValue()

    """inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we insert to the list
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
    @complexity: O(logn)
	"""

    def insert(self, i, val):

        ### DEFINING INNER-HELP METHODS FOR INSERT FUNCTION ###
        """travels from the inserted node to tree's root, while looking for criminal AVL subtree
        for every node checked, it updates it size and height.
        if there is no potential AVL criminal subtrees, it will stop and return

        @type node: AVLNode
        @param node: inserted node
        @rtype: tuple
        @returns: tuple which its first object is the last node it checked
                 and second object is number of rebalancing operations that has been done
        @complexity: O(logn)
        """

        def fixAfterInsertion(node):
            node.updateHeight()
            node.updateSize()
            curr = node.getParent()
            numOfBalancingOp = 0

            while curr != None:
                curr.updateSize()
                prevHeight = curr.getHeight()
                curr.updateHeight()

                if abs(curr.getBf()) < 2:
                    if prevHeight == curr.getHeight():
                        return (curr, numOfBalancingOp)
                    else:
                        curr = curr.getParent()
                        numOfBalancingOp += 1

                else:
                    numOfBalancingOp += insertRotate(curr)
                    return (curr, numOfBalancingOp)

            return (curr, numOfBalancingOp)

        """inserts node as a leaf without making any height or size adjustments.
        the adjustments will be done in main insert function

        @type currLeaf: AVLNode
        @param currLeaf: the leaf that we want to insert a new son to
        @type newLeaf: AVLNode
        @param newLeaf: the node that we want to insert as a new leaf
        @type direction: string
        @param direction: indicates if newLeaf will be the left or right son of currLeaf
        @pre: direction = "left" or direction = "right"
        @complexity: O(1)
        """

        def insertLeaf(currLeaf, newLeaf, direction):
            if direction == "right":  # insert newLeaf as right son of currLeaf
                virtualSon = currLeaf.getRight()
                currLeaf.completeSetRight(newLeaf)
            else:  # insert newLeaf as left son of currLeaf
                virtualSon = currLeaf.getLeft()
                currLeaf.completeSetLeft(newLeaf)

            newLeaf.completeSetRight(virtualSon)
            newLeaf.completeSetLeft(AVLNode())

        """performs rotation on AVL criminal subtree so that self will be legal AVL tree

            @type node: AVLNode
            @param node: the root of the AVL criminal subtree
            @rtype : int
            @returns: number of rebalancing operation that has been done
            @complexity: O(1)
        """

        def insertRotate(node):
            if node.getBf() == -2:
                if node.getRight().getBf() == -1:
                    self.leftRotation(node)
                    return 1
                else:
                    self.rightRotation(node.getRight())
                    self.leftRotation(node)
                    return 2

            else:
                if node.getLeft().getBf() == 1:
                    self.rightRotation(node)
                    return 1
                else:
                    self.leftRotation(node.getLeft())
                    self.rightRotation(node)
                    return 2

        ### ACTUAL STATRT OF INSERT ###

        newNode = AVLNode(val)
        if i == 0:  # inserting the minimum
            if self.empty():  # inserting the root
                self.root = newNode
                newNode.completeSetLeft(AVLNode())
                newNode.completeSetRight(AVLNode())
                self.lastItem = newNode
                self.firstItem = newNode

            else:
                if self.firstItem == None:  # handling "mikre katze" for split method which during its run the sub-trees don't have pointers to first and last
                    insertLeaf(self.findMin(), newNode, "left")
                else:
                    insertLeaf(self.firstItem, newNode, "left")
                    self.firstItem = newNode

        elif i == self.length():  # inserting the maximum
            if self.lastItem == None:
                insertLeaf(self.findMax(), newNode, "right")
            else:
                insertLeaf(self.lastItem, newNode, "right")
                self.lastItem = newNode

        else:
            curr = self.treeSelect(i+1)
            if not curr.getLeft().isRealNode():
                insertLeaf(curr, newNode, "left")
            else:
                insertLeaf(self.getPredecessorOf(curr), newNode, "right")

        curr, numOfBalancingOp = fixAfterInsertion(newNode)
        if curr != None:
            self.updateSizeAllTheWayUpFrom(curr.getParent())

        return numOfBalancingOp

    """deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
    @complexity: O(logn)
	"""

    def delete(self, i):

        ### DEFINING INNER-HELP METHODS FOR DELETE FUNCTION ###
        """
        deletes a leaf from the tree and returns the number of rebalalancing opps that had been done to fix the tree after the deletion

        @type nodeToBeDeleted: AVL node
        @param nodeToBeDeleted: A leaf which will be deleted from the tree
        @pre: nodeToBeDeleted is not the root.
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        @complexity: O(logn)
        """

        def deleteLeaf(nodeToBeDeleted):
            parent = nodeToBeDeleted.getParent()
            if parent.getLeft() == nodeToBeDeleted:
                parent.completeSetLeft(nodeToBeDeleted.getLeft())
            else:
                parent.completeSetRight(nodeToBeDeleted.getRight())
            nodeToBeDeleted.setParent(None)
            numOfBalancingOpps = self.fixTreeAfterDeletionAndJoin(parent)
            return numOfBalancingOpps

        """
        deletes a node from the tree which has only right child by bypassing it and returns the number 
        of rebalalancing opps that had been done to fix the tree after the deletion

        @type nodeToBeDeleted: AVL node
        @param nodeToBeDeleted: A node which has only right child and will be deleted from the tree
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        @complexity: O(logn)
        """

        def deleteNodeWithRightChildOnly(nodeToBeDeleted):
            parent = nodeToBeDeleted.getParent()
            child = nodeToBeDeleted.getRight()
            child.setParent(parent)
            if parent != None:  # if nodeToBeDeleted is the root then parent == None
                if parent.getLeft() == nodeToBeDeleted:
                    parent.setLeft(child)
                else:
                    parent.setRight(child)
            else:  # the nodeToBeDeleted is the root and it has only right child, that means that there are only two nodes in the tree, and now the right child becomes the root.
                self.root = child

            nodeToBeDeleted.setParent(None)
            nodeToBeDeleted.setRight(None)
            numOfBalancingOpps = self.fixTreeAfterDeletionAndJoin(parent)
            return numOfBalancingOpps

        """
        deletes a node from the tree which has only left child by bypassing it and returns the number 
        of rebalalancing opps that had been done to fix the tree after the deletion

        @type nodeToBeDeleted: AVL node
        @param nodeToBeDeleted: A node which has only left child and will be deleted from the tree
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        @complexity: O(logn)
        """

        def deleteNodeWithLeftChildOnly(nodeToBeDeleted):
            parent = nodeToBeDeleted.getParent()
            child = nodeToBeDeleted.getLeft()
            child.setParent(parent)
            if parent != None:  # if nodeToBeDeleted is the root then parent == None
                if parent.getLeft() == nodeToBeDeleted:
                    parent.setLeft(child)
                else:
                    parent.setRight(child)
            else:  # the nodeToBeDeleted is the root and it has only left child, that means that there are only two nodes in the tree, and now the left child becomes the root.
                self.root = child

            nodeToBeDeleted.setParent(None)
            nodeToBeDeleted.setLeft(None)
            numOfBalancingOpps = self.fixTreeAfterDeletionAndJoin(parent)
            return numOfBalancingOpps

        ### ACTUAL START OF DELETE ֳֳ###

        if i < 0 or i >= self.length():
            return -1

        if self.length() == 1:  # there is only one item in the list and we are deleting it
            self.root = None
            self.firstItem = None
            self.lastItem = None
            return 0

        nodeToBeDeleted = self.treeSelect(i+1)

        if i == 0:  # updating first because deleting the first item in the list
            self.firstItem = self.getSuccessorOf(nodeToBeDeleted)

        if i == self.length() - 1:  # updating last because deleting the last item in the list
            self.lastItem = self.getPredecessorOf(nodeToBeDeleted)

        if nodeToBeDeleted.getSize() == 1:  # the node is a leaf
            numOfBalancingOpps = deleteLeaf(nodeToBeDeleted)
            return numOfBalancingOpps

        if not nodeToBeDeleted.getLeft().isRealNode():  # the node has only right child
            numOfBalancingOpps = deleteNodeWithRightChildOnly(nodeToBeDeleted)
            return numOfBalancingOpps

        if not nodeToBeDeleted.getRight().isRealNode():  # the node has only left child
            numOfBalancingOpps = deleteNodeWithLeftChildOnly(nodeToBeDeleted)
            return numOfBalancingOpps

        # the node has two children
        successor = self.getSuccessorOf(nodeToBeDeleted)
        if successor.size == 1:
            numOfBalancingOpps = deleteLeaf(successor)
        else:  # the successor doesn't have a left son.
            numOfBalancingOpps = deleteNodeWithRightChildOnly(successor)

        # putting the successor in nodeToBeDeleted place
        parent = nodeToBeDeleted.getParent()
        leftChild = nodeToBeDeleted.getLeft()
        rightChild = nodeToBeDeleted.getRight()
        if parent != None:  # if nodeToBeDeleted is the root then parent == None
            if parent.getLeft() == nodeToBeDeleted:
                parent.setLeft(successor)
            else:
                parent.setRight(successor)
        else:
            self.root = successor
        successor.setParent(parent)
        successor.completeSetLeft(leftChild)
        successor.completeSetRight(rightChild)
        successor.updateHeight()
        successor.updateSize()
        nodeToBeDeleted.setLeft(None)
        nodeToBeDeleted.setRight(None)
        nodeToBeDeleted.setParent(None)
        return numOfBalancingOpps

    """returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
    @complexity: O(1)
	"""

    def first(self):
        if self.empty():
            return None
        return self.firstItem.getValue()

    """returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
    @complexity: O(1)
	"""

    def last(self):
        if self.empty():
            return None
        return self.lastItem.getValue()

    """returns an array representing list

	@rtype: list
	@returns: a list of strings representing the data structure
    @complexity: O(n)
	"""

    def listToArray(self):
        def recList2Arr(node, res):
            if node.isRealNode():
                recList2Arr(node.getLeft(), res)
                res.append(node.getValue())
                recList2Arr(node.getRight(), res)

        res = []
        if self.empty():
            return res
        recList2Arr(self.getRoot(), res)
        return res

    """returns the size of the list

	@rtype: int
	@returns: the size of the list
    @complexity: O(1)
	"""

    def length(self):
        if self.empty():
            return 0
        return self.getRoot().getSize()

    """splits the list at the i'th index

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list according to whom we split
	@rtype: list
	@returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
	right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    @complexity: O(logn)
	"""

    def split(self, i):
        splitter = self.treeSelect(i+1)
        L1 = AVLTreeList()
        L1.root = splitter.getLeft() if splitter.getLeft().isRealNode() else None
        splitter.getLeft().setParent(None)
        L2 = AVLTreeList()
        L2.root = splitter.getRight() if splitter.getRight().isRealNode() else None
        splitter.getRight().setParent(None)

        prev = splitter
        curr = splitter.getParent()

        while curr != None:
            parent = curr.getParent()
            curr.setParent(None)
            if curr.getLeft() == prev:  # if we went up-right
                rightTree = AVLTreeList()
                rightTree.root = curr.getRight() if curr.getRight().isRealNode() else None
                curr.getRight().setParent(None)
                L2.join(curr, rightTree)
            if curr.getRight() == prev:  # if we went up-left
                leftTree = AVLTreeList()
                leftTree.root = curr.getLeft() if curr.getLeft().isRealNode() else None
                curr.getLeft().setParent(None)
                leftTree.join(curr, L1)
                L1 = leftTree
            prev = curr
            curr = parent

        if not L1.empty():
            L1.firstItem = L1.findMin()
            L1.lastItem = L1.findMax()
        else:
            L1.firstItem = None
            L1.lastItem = None
        if not L2.empty():
            L2.lastItem = L2.findMax()
            L2.firstItem = L2.findMin()
        else:
            L2.lastItem = None
            L2.firstItem = None

        self.root = None
        self.firstItem = None
        self.lastItem = None

        return [L1, splitter.getValue(), L2]

    """concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
    @complexity: O(logn) when n is the mutual length of self and lst
	"""

    def concat(self, lst):
        heightDifference = abs(self.getTreeHeight() - lst.getTreeHeight())
        if self.empty():
            self.firstItem = lst.firstItem
            self.lastItem = lst.lastItem
            self.root = lst.getRoot()
        else:
            connector = self.lastItem
            self.delete(self.length()-1)
            self.join(connector, lst)
        return heightDifference

    """searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
    @complexity: O(n)
	"""

    def search(self, val):
        candidate = self.firstItem
        index = 0
        while candidate != None:
            if candidate.getValue() == val:
                return index
            index += 1
            candidate = self.getSuccessorOf(candidate)
        return -1

    """returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
    @complexity: O(1)
	"""

    def getRoot(self):
        return self.root

    ### SERVICE METHODS ###

    """returns the i'th smallest node in the tree

    @type i: int
    @pre: 1 <= i <= self.length()
    @param i: a position in the tree
    @rtype: AVLNode
    @returns: the i'th smallest node in the tree
    @complexity: O(logi)
    """

    def treeSelect(self, i):
        if i == 1:
            return self.firstItem
        if i == self.length():
            return self.lastItem

        curr = self.findSmallestSubTreeOfSize(i)
        r = curr.getLeft().getSize() + 1
        while (i != r):
            if i < r:               # the node is in the left tree so we need to look for the i'th smallest node in the left tree
                curr = curr.getLeft()

            # the node is in the right tree so we need to look for the (i-r)'th smallest node in the right tree
            else:
                curr = curr.getRight()
                i = i - r
            r = curr.getLeft().getSize() + 1
        return curr

    """returns the smallest node in the tree whose subtree of size >= k

    @type k: int
    @pre: 1 <= k <= self.length()
    @rtype: AVLNode
    @returns: the smallest node off size >= k
    @complexity: O(logk)
    """

    def findSmallestSubTreeOfSize(self, k):
        curr = self.firstItem
        while (curr.getSize() < k):
            curr = curr.getParent()
        return curr

    """returns the successor of a given node

    @type node: AVLNode
	@rtype: AVLNode
	@returns: the successor of a given node. if the node is the Maximum returns None
    @complexity: O(logn)
	"""

    def getSuccessorOf(self, node):
        if self.lastItem == node:
            return None

        if node.getRight().isRealNode():
            subTree = AVLTreeList()
            subTree.root = node.getRight()
            return subTree.findMin()

        curr = node.getParent()
        # breaks when turning right for the first time
        while (curr != None) and (curr.getRight() == node):
            node = curr
            curr = curr.getParent()
        return curr

    """returns the predecessor of a given node

    @type node: AVLNode
	@rtype: AVLNode
	@returns: the predecessor of a given node. if the node is the minimum returns None
    @complexity: O(logn)
	"""

    def getPredecessorOf(self, node):
        if node == self.firstItem:
            return None
        if node.getLeft().isRealNode():
            subTree = AVLTreeList()
            subTree.root = node.getLeft()
            return subTree.findMax()

        curr = node.getParent()
        # breaks when turning left for the first time
        while (curr != None) and (curr.getLeft() == node):
            curr = curr.getParent
        return curr

    """
    updating the size of all the nodes which are in the path from node to the root

    @type node: AVLNode
    @complexity: O(logn)
    """

    def updateSizeAllTheWayUpFrom(self, node):
        while (node != None):
            node.updateSize()
            node = node.getParent()

    """given that the node is an AVL criminal with BF = +2 and its left son has BF = +1,
    fixes the Bf of node. furthermore, updating the height and size fields of the nodes involved
    @complexity: O(1)
	"""

    def rightRotation(self, node):
        B = node
        parent = B.getParent()
        A = B.getLeft()
        if parent != None:  # if B is the root then parent == None
            if parent.getLeft() == B:
                parent.setLeft(A)
            else:
                parent.setRight(A)
        else:
            self.root = A
        A.setParent(parent)
        B.setParent(A)
        B.setLeft(A.getRight())
        A.setRight(B)
        B.getLeft().setParent(B)

        # fixing height field off A and B, the only nodes whose height was changed
        B.updateHeight()
        A.updateHeight()

        # fixing size field off A and B, the only nodes whose size was changed
        B.updateSize()
        A.updateSize()

    """given that node is an AVL criminal with BF = -2 and its right son has BF = -1,
    fixes the Bf of node. furthermore, updating the height and size fields of the nodes involved
    @complexity: O(1)
	"""

    def leftRotation(self, node):
        B = node
        parent = B.getParent()
        A = B.getRight()
        if parent == None:
            self.root = A
            A.setParent(None)
        else:
            if parent.getLeft() == B:
                parent.completeSetLeft(A)
            else:
                parent.completeSetRight(A)
        B.completeSetRight(A.getLeft())
        A.completeSetLeft(B)

        # fixing height field off A and B, the only nodes whose height was changed
        B.updateHeight()
        A.updateHeight()

        # fixing size field off A and B, the only nodes whose size was changed
        B.updateSize()
        A.updateSize()

    """
    travels from the parrent of the delted node or the parent of the connector to tree's root, 
    while looking for criminal AVL subtrees and handling the criminals by preforming the rotations needed.
    for every node in the path to the root, it updates its size and height, if needed.
    returns the number of rebalancing operation due to AVL rebalancing.
    
    @type node: AVLNode
    @param node: the parent of the deleted node or the parent of the connector
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing.
    @complexity: O(h1 - h2 + 1) = O(logn) when h1 is the tree height and h2 is the height of node.
    """

    def fixTreeAfterDeletionAndJoin(self, node):
        numOfBalancingOpps = 0
        doneWithFixingHeight = False
        while node != None:
            originalParent = node.getParent()
            node.updateSize()
            if not doneWithFixingHeight:
                BF = node.getBf()
                heightBefore = node.getHeight()
                node.updateHeight()
                heightAfter = node.getHeight()
                if abs(BF) < 2 and heightAfter == heightBefore:
                    doneWithFixingHeight = True

                elif abs(BF) < 2 and heightAfter != heightBefore:
                    numOfBalancingOpps += 1
                else:  # abs(BF) = 2
                    if BF == 2:
                        BFL = node.getLeft().getBf()
                        if BFL == 1 or BFL == 0:
                            self.rightRotation(node)
                            numOfBalancingOpps += 1
                        elif BFL == - 1:
                            self.leftRotation(node.getLeft())
                            self.rightRotation(node)
                            numOfBalancingOpps += 2
                    else:  # BF = -2
                        BFR = node.getRight().getBf()
                        if BFR == -1 or BFR == 0:
                            self.leftRotation(node)
                            numOfBalancingOpps += 1
                        elif BFR == 1:
                            self.rightRotation(node.getRight())
                            self.leftRotation(node)
                            numOfBalancingOpps += 2

            node = originalParent

        return numOfBalancingOpps

    """
    inserts val at the end of the list

	@param val: the value we insert to the end of the list
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
    @complexity: O(logn)
    """

    def append(self, val):
        return self.insert(self.length(), val)

    """merges two AVL trees

    @type connector: AVL node
    @type L2: AVL tree
    @pre connector.isRealNode()
    @complexity: O(abs(self.getTreeHeight() - L2.getTreeHeight()) + 1)
    """

    def join(self, connector, L2):
        if L2.empty():
            self.append(connector.getValue())
            return
        elif self.empty():
            L2.insert(0, connector.getValue())
            self.firstItem = L2.firstItem
            self.lastItem = L2.lastItem
            self.root = L2.getRoot()
            return

        elif self.getRoot().getHeight() == L2.getRoot().getHeight():
            connector.completeSetLeft(self.getRoot())
            connector.completeSetRight(L2.getRoot())
            connector.setParent(None)
            self.root = connector

        elif self.getRoot().getHeight() < L2.getRoot().getHeight():
            curr = L2.getRoot()
            while curr.getHeight() > self.getRoot().getHeight():
                curr = curr.getLeft()
            currParent = curr.getParent()
            connector.completeSetLeft(self.getRoot())
            connector.completeSetRight(curr)
            currParent.completeSetLeft(connector)
            self.root = L2.getRoot()

        else:
            curr = self.getRoot()
            while curr.getHeight() > L2.getRoot().getHeight():
                curr = curr.getRight()
            currParent = curr.getParent()
            connector.completeSetLeft(curr)
            connector.completeSetRight(L2.getRoot())
            currParent.completeSetRight(connector)
        self.lastItem = L2.lastItem
        connector.updateSize()
        connector.updateHeight()
        if self.getRoot() != connector:
            self.fixTreeAfterDeletionAndJoin(connector.getParent())

    """
    returns the node which contains the last item in the AVLtreelist not using the pointer to it. if empty returns None.

    @rtype: AVLNode
    @complexity: O(logn)
    """

    def findMax(self):
        curr = self.getRoot()
        if curr == None:
            return None
        while(curr.getRight().isRealNode()):
            curr = curr.getRight()
        return curr

    """
    returns the node which contains the first item in the AVLtreelist not using the pointer to it. if empty returns None.

    @rtype: AVLNode
    @complexity: O(logn)
    """

    def findMin(self):
        curr = self.getRoot()
        if curr == None:
            return None
        while (curr.getLeft().isRealNode()):
            curr = curr.getLeft()
        return curr

    def getTreeHeight(self):
        if self.empty():
            return -1
        else:
            return self.getRoot().getHeight()

    ### PRINT TREE FUNCTIONS ###

    def printt(self):
        out = ""
        for row in self.printree(self.root):  # need printree.py file
            out = out + row + "\n"
        print(out)

    def printree(self, t, bykey=True):
        """Print a textual representation of t
        bykey=True: show keys instead of values"""
        # for row in trepr(t, bykey):
        #        print(row)
        return self.trepr(t, False)

    def trepr(self, t, bykey=False):
        """Return a list of textual representations of the levels in t
        bykey=True: show keys instead of values"""
        if t == None:
            return ["#"]

        thistr = str(t.key) if bykey else str(t.getValue())

        return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

    def conc(self, left, root, right):
        """Return a concatenation of textual represantations of
        a root node, its left node, and its right node
        root is a string, and left and right are lists of strings"""

        lwid = len(left[-1])
        rwid = len(right[-1])
        rootwid = len(root)

        result = [(lwid+1)*" " + root + (rwid+1)*" "]

        ls = self.leftspace(left[0])
        rs = self.rightspace(right[0])
        result.append(ls*" " + (lwid-ls)*"_" + "/" + rootwid *
                      " " + "\\" + rs*"_" + (rwid-rs)*" ")

        for i in range(max(len(left), len(right))):
            row = ""
            if i < len(left):
                row += left[i]
            else:
                row += lwid*" "

            row += (rootwid+2)*" "

            if i < len(right):
                row += right[i]
            else:
                row += rwid*" "

            result.append(row)

        return result

    def leftspace(self, row):
        """helper for conc"""
        # row is the first row of a left node
        # returns the index of where the second whitespace starts
        i = len(row)-1
        while row[i] == " ":
            i -= 1
        return i+1

    def rightspace(self, row):
        """helper for conc"""
        # row is the first row of a right node
        # returns the index of where the first whitespace ends
        i = 0
        while row[i] == " ":
            i += 1
        return i

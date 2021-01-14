
from Element import *
from copy import copy

empty_queue = None

class QueueZero(object):

    def __init__(self, head, tail, lendiff):
        self.head = head
        self.tail = tail
        self.lendiff = lendiff #  = |head| - |tail|
        self.state = 0


def enqueue_zero(q, value):
    if q.head is None and q.tail is None:
        return QueueZero(Element(value, None), q.tail, 1)

    if q.lendiff == 0:
        return enqueue_one(QueueOne(q.head, q.head, q.tail, None, None, None, 0, 0), value)

    n_tail = Element(value, q.tail)
    q.lendiff -= 1
    return QueueZero(q.head, n_tail, q.lendiff)


def dequeue_zero(q):
    if q.head is None:
        return None, empty_queue
    if q.lendiff == 0:
        return dequeue_one(QueueOne(q.head, q.head, q.tail, None, None, None, 0, 0))

    q.lendiff -= 1
    n_queue = QueueZero(q.head.next, q.tail, q.lendiff)
    return q.head.value, n_queue




class QueueOne(object):

    def __init__(self, head_origin, head, tail, head_reversed, n_head, n_tail, lendiff, delta_for_copy):
        self.head_origin = head_origin
        self.head = head
        self.tail = tail
        self.head_reversed = head_reversed
        self.n_head = n_head
        self.n_tail = n_tail
        self.lendiff = lendiff
        self.delta_for_copy = delta_for_copy
        self.state = 1



def enqueue_one(q, value):
    n_tail = Element(value, q.n_tail)
    lendiff = q.lendiff-1
    
    
    head = q.head
    tail = q.tail
    head_reversed = q.head_reversed
    n_head = q.n_head
    delta_for_copy = q.delta_for_copy
    
    #copy
    for _ in range(2):
        if head is not None:
            head_reversed = Element(head.value, head_reversed)
            head = head.next
            #copy from head to head_reversed *2 -> #copy+2 
            delta_for_copy +=1
        if tail is not None:
            n_head = Element(tail.value, n_head)
            tail = tail.next
            #copy from tail to n_head *2 -> lendiff+2
            lendiff +=1
        if head is None and tail is None:
            return QueueTwo(q.head_origin, head_reversed, n_head, n_tail, lendiff, delta_for_copy)
            
    
    return QueueOne(q.head_origin, head, tail, head_reversed, n_head, n_tail, lendiff, delta_for_copy)
    #new_n_tail = Element(value, q.tail) -> lendiff-1
    #podminka till tail none
    #copy from tail to n_head *2 -> lendiff+2
    #podminka till head none
    #copy from head to head_reversed *2 -> #copy+2 
    # return new Queue1
    


def dequeue_one(q):

    head_origin = q.head_origin.next
    delta_for_copy = q.delta_for_copy-1
    
    
    head = q.head
    tail = q.tail
    head_reversed = q.head_reversed
    n_head = q.n_head
    lendiff = q.lendiff

    for _ in range(2):
        if head is not None:
            head_reversed = Element(head.value, head_reversed)
            head = head.next            
            #copy from head to head_reversed *2 -> #copy+2 
            delta_for_copy +=1
        if tail is not None:
            n_head = Element(tail.value, n_head)
            tail = tail.next            
            #copy from tail to n_head *2 -> lendiff+2
            lendiff +=1
        if head is None and tail is None:
            return q.head_origin.value, QueueTwo(head_origin, head_reversed, n_head, q.n_tail, lendiff, delta_for_copy)

    return q.head_origin.value, QueueOne(head_origin, head, tail, head_reversed, n_head, q.n_tail, lendiff, delta_for_copy)
    #new_head_origin = head_origin.next #copy-1
    
    #podminka till tail none
    #copy from tail to n_head *2 -> lendiff+2
    #podminka till head none
    #copy from head to head_reversed *2 -> #copy+2 
    # return new Queue1


class QueueTwo(object):
    
    def __init__(self, head_origin, head_reversed, n_head, n_tail, lendiff, delta_for_copy):
        self.head_origin = head_origin
        self.head_reversed = head_reversed
        self.n_head = n_head
        self.n_tail = n_tail
        self.lendiff = lendiff
        self.delta_for_copy = delta_for_copy
        self.state = 2

    def __str__(self):

        return "{} {} {}".format(self.head_origin, self.n_tail, self.n_tail.next)    
    

def enqueue_two(q, value):

    n_tail = Element(value, q.n_tail)
    lendiff = q.lendiff-1
    
    head_reversed = q.head_reversed
    n_head = q.n_head
    delta_for_copy = q.delta_for_copy

    
    for _ in range(2):
        if delta_for_copy == 0:
            return QueueZero(n_head,n_tail,lendiff)
        else:
            n_head = Element(head_reversed.value, n_head)
            head_reversed = head_reversed.next
            #napojit prvek z head_reversed do n_head * 2 -> lendiff+2 #copy-2
            lendiff +=1
            delta_for_copy -=1

    return QueueTwo(q.head_origin, head_reversed, n_head, n_tail, lendiff, delta_for_copy)
    #vlozit prvek do n_tail lendiff -1
    #napojit prvek z head_reversed do n_head * 2 -> lendiff+2 #copy-2
    
    


def dequeue_two(q):

    head_origin = q.head_origin.next
    delta_for_copy = q.delta_for_copy-1
    
    head_reversed = q.head_reversed
    n_head = q.n_head
    lendiff = q.lendiff

    #copy
    for _ in range(2):
        if delta_for_copy == 0:
            return q.head_origin.value, QueueZero(n_head,q.n_tail,lendiff)
        else:
            n_head = Element(head_reversed.value, n_head)
            head_reversed = head_reversed.next            
            #napojit prvek z head_reversed do n_head * 2 -> lendiff+2 #copy-2
            lendiff +=1
            delta_for_copy -=1
    
    return q.head_origin.value, QueueTwo(head_origin, head_reversed, n_head, q.n_tail, lendiff, delta_for_copy)
    # odebrat prvek s head_origin #copy -1
    #napojit prvek z head_reversed do n_head * 2 -> lendiff+2 #copy-2
    # kdyz je #copy 0 vratit queue0 s head, tail a lendiff 
    # pokud ne vratit na konci stejnou tridu s novymi param
    

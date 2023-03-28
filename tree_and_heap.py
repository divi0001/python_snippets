from ast import Delete
from logging import exception
import random

def empty() :
    return [] 

def node(l,v,r) :
    return [l,v,r]

def leaf(v) :
    return node(empty(),v,empty())

def is_empty(tree) :
    return tree == []

def left(tree) :
    return tree[0]

def value(tree) :
    return tree[1]

def right(tree) :
    return tree[2]

def update_node(new_tree,tree) :
    tree[:] = new_tree

def update_value(v,tree) :
    tree[1] = v

def clear_node(t) :
    t[:] = []
    
def tree_at(path,tree) :
    if len(path) == 0 :
        return tree
    elif is_empty(tree) :
        return None
    elif path[0]=='l' :
        return tree_at(path[1:],left(tree))
    else :
        return tree_at(path[1:],right(tree))

def elem(pos,heap):
        if heap == empty():
            return False
        elif pos == "":
            return True
        elif pos[0] == "l":
            return elem(pos[1:],left(heap))
        elif pos[0] == "r":
            return elem(pos[1:],right(heap))
    
# mutate value in tree at given positon (path)
def update_value_at(path,v,tree) :
    if len(path) == 0 :
        update_value(v,tree)
    elif is_empty(tree) :
        return None
    elif path[0]=='l' :
        return update_value_at(path[1:],v,left(tree))
    else :
        return update_value_at(path[1:],v,right(tree))

# replace complete subtree in tree at given postion (path)
def update_tree_at(path,new_tree,tree) :
    if len(path) == 0 :
        # return update_node(new_tree,tree) # Achtung, s.u,
        return update_node(copy_tree(new_tree), tree)
    elif is_empty(tree) :
        return None
    elif path[0]=='l' :
        return update_tree_at(path[1:],new_tree,left(tree))
    else :
        return update_tree_at(path[1:],new_tree,right(tree))


def copy_tree(tree) :
    if is_empty(tree) :
        return empty()
    else :
        return node(copy_tree(left(tree)), value(tree), copy_tree(right(tree)))
    
def next_pos(path) :
    res = ''
    i = len(path) - 1
    while i >= 0 and path[i] != 'l':
        res = 'l' + res
        i = i - 1
    if i < 0 :
        res = 'l' + res
    else :
        res = path[0:i] + 'r' + res
    return res

def prev_pos(path) :
    res = ''
    i = len(path) - 1
    while i >= 0 and path[i] != 'r':
        res = 'r' + res
        i = i - 1
    if i < 0 :
        res = res[1:]
    else :
        res = path[0:i] + 'l' + res
    return res

def direct(t,dir) :
    return left(t) if dir == 'l' else right(t)

def empty_siced_heap() :
    return { 'next_pos' : '', 'heap' : empty() }

def is_empty_siced_heap(siced_heap) :
    return siced_heap['next_pos'] == ''

def add(v,siced_heap) :
    
    def add_h(path,v,heap) :
        if path == '' :  # we know, that here is an empty node
            update_node(leaf(v),heap)
        else :
            child_heap = direct(heap,path[0])
            add_h(path[1:],v,child_heap)
            child_val = value(child_heap)
            if child_val < value(heap) :
                update_value(value(heap),child_heap)
                update_value(child_val,heap)
                
    pos = siced_heap['next_pos']
    heap = siced_heap['heap']
    add_h(pos,v,heap)
    siced_heap['next_pos'] = next_pos(pos)
    
def extract_min(siced_heap) :
    
    
    
    def extract_last_elem(path,heap) :
        if len(path) == 0 :
            val = value(heap)
            clear_node(heap)
            return val
        else :
            child = direct(heap, path[0])
            return extract_last_elem(path[1:],child)
        
    def find_min_sub_heap(heap) :
        left_heap = left(heap)
        right_heap = right(heap)
        if is_empty(left_heap) :
            return None
        elif is_empty(right_heap) :
            return left_heap
        else :
            left_val = value(left_heap)
            right_val = value(right_heap)
            return left_heap if left_val < right_val else right_heap
        
    def heapify_down(heap) :
        if not is_empty(heap) :
            val = value(heap)
            min_sub_heap = find_min_sub_heap(heap)
            if min_sub_heap != None :
               child_val = value(min_sub_heap)
               if child_val < val :
                    update_value(val,min_sub_heap)
                    update_value(child_val,heap)
                    heapify_down(min_sub_heap)        

    heap = siced_heap['heap']
    
    if is_empty(heap) :
        return None
    else:
        path = prev_pos(siced_heap['next_pos'])
        min = value(heap)
        new_val = extract_last_elem(path,heap)
        if not is_empty(heap) :
            update_value(new_val,heap)
            heapify_down(heap)
        siced_heap['next_pos'] = path
    return min

heap = empty_siced_heap()

for i in range(10) :
    add(random.randint(0,20),heap)
print(heap)


    
    
def delete(pos,heap):
    
    def delete_h(pos,heap):
        if pos == "":
            try:
                while True:
                    pos = next_pos(pos)
                    tree = tree_at(pos,heap)
                    if tree == empty():
                        e = exception("Last Pos reached")
                        raise e
            except:
                pos = prev_pos(pos)
                heap[1] = value(tree_at(pos,heap))
                update_value_at(pos,[],heap)
            
        else:
            if pos == 'l':
                delete_h(pos[1:],left(heap))
            else:
                delete_h(pos[1:],right(heap))
    
    
    def correct_heapatitis(heap,dire):
        if dire == 'l':
            if value(heap) > value(left(heap)):
                c = value(left(heap))
                value(left(heap))[:] = value(heap)
                value(heap)[:] = c
                return True
            else:
                return False
        elif dire == "r":
            if value(heap) > value(right(heap)):
                c = value(right(heap))
                value(right(heap))[:] = value(heap)
                value(heap)[:] = c
                return True
            else:
                return False
            
            
            
    def heapatitis(pos,heap):
        
        if pos == "":
            return heap
        if pos == "l":
            correct_heapatitis(heap,'l')
            return heapatitis(pos[1:],left(heap))
        else:
            correct_heapatitis(heap,'r')
            return heapatitis(pos[1:],right(heap))
    
    pos_copy = pos + ''
    
    if elem(pos,heap):
    
        delete_h(pos_copy,heap)
        heap = heapatitis(pos,heap)
        return True

    else:
        return False        
        
                
heapy = [[[[[], 19, []], 11, [[], 13, []]], 2, [[[], 18, []], 15, []]], 2, [[[], 6, []], 2, [[], 16, []]]]
heapa = [[[[[], 16, []], 5, [[], 16, []]], 4, [[], 9, []]], 1, [[[], 8, []], 2, [[], 17, []]]]

delete('l',heapy)

min = extract_min(heap)
print(min,heap)


print(value(heapa),value(left(heapa)),value(right(heapa)),value(left(heapa)),value(left(left(heapa))),value(left(right(heapa))),value(right((heapa))),value(right(left(heapa))))
print(right(left(left(heapy))))
try:
    pos1 = ''
    while True:
        pos1 = next_pos(pos1)
        print(tree_at(pos1,heapy))  
        if not tree_at(pos1,heapy):
            ee = exception("Ende im Gelände")
            raise ee
except:
    pass

#Dies wird keinen korrekten Heap zurückgeben, da die next_pos Funktion nicht den kompletten Baum durchiterieren kann, da die add Funktion keinen validen Heap aufbaut (es existieren leere Elemente,
#wo keine sein dürften). Im Worst Case ist unsere Laufzeit aus O(n^2), wenn der komplette Baum durchlaufen werden muss, um den zu löschenden Wert zu finden. Da dies dann log(n) Schritte
# in Abhängigkeit der größe unserer Liste darstellt. (vernachlässigbar)  Für das finden der letzten Position müsste man im Worst Case dann n Schritte ausführen.
# Zuletzt müssen wir die Heapeigenschaft wiederherstellen. Da wir dies nur auf der Seite machen müssen, auf der wir den Wert verändert haben, hat dies im Worst Case eine Laufzeit aus O(log(n)).
# Dies kann auch vernachlässigt werden. Außerdem müssen wir überprüfen, ob der Wert überhaupt im Baum vorhanden ist. Im schlimmsten Fall braucht auch dies n Schritte.




def remove(v,heap):
    pos = ""
    
    try:    
        while not value(tree_at(pos,heap)) == v:
            pos = next_pos(pos)
        delete(pos,heap)
        return True
    except:
        return False
    
#Dies hat die Laufzeit von delete und elem, und müsste im Worst Case einmal durch den Baum iterieren (O(n^2) und O(n) und O(n)) also ingesamt im Worst Case O(n^4)
#zum Testen bitte den zweiten Code auskommentieren, die Funktionsnamen wiederholen sich ja wie gefordert...
remove(1,heapa)
print(heapa)

from logging import exception
import random

def empty_heap() :
    return []

def swap(l,i,j) :
    h = l[i]
    l[i] = l[j]
    l[j] = h
    
def add(v,heap) :
    heap.append(v)
    i = len(heap) - 1
    next_i = (i - 1) // 2
    while i > 0 and heap[i] < heap[next_i] :
        swap(heap,i,next_i)
        i = next_i
        next_i = (i - 1) // 2

def min_subtree(i,heap) :
    left = 2 * i + 1
    right = 2 * i + 2
    if left >= len(heap) :
        return None
    elif right >= len(heap) or heap[left] < heap[right] :
        return left
    else :
        return right
    
def extract_min(heap) :
    if len(heap) == 0 :
        return None
    else :
        min = heap[0]
        swap(heap,0,len(heap)-1)
        heap[len(heap)-1:] = []
        i = 0
        min_child_pos = min_subtree(i,heap)
        while min_child_pos != None and heap[min_child_pos] < heap[i] :
            swap(heap,min_child_pos,i)
            i = min_child_pos
            min_child_pos = min_subtree(i,heap)
        return min

heap = empty_heap()



def delete(pos,heap):
    
    i = 0
    try:
        z = True
        while z:

            if pos[0] == "l":
                i = i * 2 + 1
                pos = pos[1:]
            
            elif pos[0] == "r":
                i = i * 2 + 2
                pos = pos[1:]
            
            if len(pos) == 0 and heap[i]:                
                swap(heap,i,len(heap) - 1)
                heap[:] = heap[:len(heap) - 1]
                
                while i * 2 + 1 < len(heap) - 1:
                    
                    if heap[i] > heap[i * 2 + 1]:
                        swap(heap,i,i * 2 + 1)
                    if heap[i] > heap[i * 2 + 2]:
                        swap(heap,i,i * 2 + 2)
                    i += 1
                
        
            elif pos == "" and not heap[i]:
                eeee = exception("not found")
                raise eeee
                
    except:
        return False
    else:
        return True


heapy = [2, 2, 2, 6, 15, 11, 13, 18, 16, 19]
aheap = [2, 2, 2, 16, 15, 11, 13, 19, 18]
delete('ll',heapy)
print(heapy)

#Im Worst Case ist die Position im Heap log(n) Schritt in Abhängigkeit von der Listenlänge. Dies brauchen wir dann auch, um festzustellen, ob das Element in der Liste ist. Indem Fall wäre allerdings das wieder-
#herstellen der Heapeigenschaft aus O(1), da wir dann ja schon in einem Blatt des Heaps sind. Anders herum, wenn wir das Element direkt finden, würde die Heapify Funktion log(n) Schritte brauchen.
#Wir haben also im Worst Case immer eine Laufzeit aus  O(log(n)). Tatsächlich haben wir nach genauer Betrachtung immer eine Laufzeit aus O(log(n)), da das was man nicht an Laufzeit für das finden des Elements
#benötigt automatisch für die Wiederherstellung der Heapeigenschaft draufgeht.


def remove(v,heap):
    k = 0
    K = False
    for elem in heap:
        
        if elem == v:
            K = k
        else:
            k += 1
    if not K:
        return False
    swap(heap,K,len(heap) - 1)
    heap[:] = heap[:len(heap) - 1]
    i = K
    while i * 2 + 1 < len(heap) - 1:
                    
        if heap[i] > heap[i * 2 + 1]:
            swap(heap,i,i * 2 + 1)
        if heap[i] > heap[i * 2 + 2]:
            swap(heap,i,i * 2 + 2)
        i += 1
    return True


print(aheap)
remove(11,aheap)
print(aheap)

#Im Worst Case ist das Element ganz hinten in der Liste. Und ja, theoretisch könnten wir auch gucken, ob das Element auf einer rechts/links von Ebene eines Elements ist, und abbrechen, wenn alle Elemente bereits
# größer sind, das macht im Worst Case aber effektiv keinen Unterschied. Wir laufen dann n Schritte (n in Abhängigkeit der Listengröße) durch die Liste, und haben wieder einen downHeap aus O(1) analog zur oberen
# Funktion. Anders als bei Baumimplementierungen verändert sich die Laufzeit nicht abhängig davon, ob man mit Pfaden oder Elementen arbeitet, da man in Listen mit beidem ähnlich schnell ist. Insgesamt als aus O(n).


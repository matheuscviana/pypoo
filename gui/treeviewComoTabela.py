"""A directory browser using Ttk Treeview.
 
Based on the demo found in Tk 8.5 library/demos/browse
"""
import os
import glob
import tkinter
from tkinter import ttk
 
#  funções auxiliares ..........................
 
def populate_roots(tree):
    dir = os.path.abspath('.').replace('\\', '/')
    node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
    populate_tree(tree, node)
 
 
# esta função insere os caminhos do arquivo no widget Treeview
def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return
 
    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))
 
    parent = tree.parent(node)
    special_dirs = [] if parent else glob.glob('.') + glob.glob('..')
 
    for p in special_dirs + os.listdir(path):
        ptype = None
        p = os.path.join(path, p).replace('\\', '/')
        if os.path.isdir(p): ptype = "directory"
        elif os.path.isfile(p): ptype = "file"
 
        fname = os.path.split(p)[1]
        id = tree.insert(node, "end", text=fname, values=[p, ptype])
 
        if ptype == 'directory':
            if fname not in ('.', '..'):
                tree.insert(id, 0, text="dummy")
                tree.item(id, text=fname)
        elif ptype == 'file':
            size = os.stat(p).st_size
            tree.set(id, "size", "%d bytes" % size)
 
 
#esta função atualiza a árvore quando o usuario abre um diretorio
def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())
 
#esta função atualiza a arvore qdo o diretório clica duas vezes no mouse
def change_dir(event):
    tree = event.widget
    node = tree.focus()
    if tree.parent(node):
        path = os.path.abspath(tree.set(node, "fullpath"))
        if os.path.isdir(path):
            os.chdir(path)
            tree.delete(tree.get_children(''))
            populate_roots(tree)
 
 
 
def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)
 
 
# corpo do programa principal  .....................
 
#criamos um objeto tkinter
root = tkinter.Tk()
 
#criamos barras horizontais
vsb = ttk.Scrollbar(orient="vertical")
hsb = ttk.Scrollbar(orient="horizontal")
 
# criamos um objeto Treeview
tree = ttk.Treeview(columns=("fullpath", "type", "size"),
    displaycolumns="size", yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
    xscrollcommand=lambda f, l:autoscroll(hsb, f, l))
 
# associamos as barras de scroll às vistas x e y do objeto Treeview
vsb['command'] = tree.yview
hsb['command'] = tree.xview
 
# define os cabeçalhos das diferentes colunas
tree.heading("#0", text="Directory Structure", anchor='w')
tree.heading("size", text="File Size", anchor='w')
tree.column("size", stretch=0, width=100)
 
# inicializa a Treeview
populate_roots(tree)
 
#associa os eventos do Treeview a métodos especificos
tree.bind('<<TreeviewOpen>>', update_tree)
tree.bind('<Double-Button-1>', change_dir)
 
# Arrange the tree and its scrollbars in the toplevel
tree.grid(column=0, row=0, sticky='nswe')
vsb.grid(column=1, row=0, sticky='ns')
hsb.grid(column=0, row=1, sticky='ew')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
 
root.mainloop()
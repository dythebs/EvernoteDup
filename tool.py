from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
'''
将印象笔记中的笔记转移到evernote中
1.初始化两个账户
2.复制笔记本列表
3.复制标签列表
4.复制笔记
'''
#两个账户的token
source_dev_token = 'source account token'
dest_dev_token = 'destination account token'
#获取某一个笔记本下的全部笔记
def getNotesByNotebookGuid(noteStore,notebookGuid):
	f = NoteStore.NoteFilter()
	f.notebookGuid = notebookGuid
	return noteStore.findNotes(f, 0, 999).notes
#从笔记本列表中按名查找笔记本的guid
def getGuidByNotebookName(notebookName,notebooksList):
	for notebook in notebooksList:
		if notebook.name == notebookName:
			return notebook.guid
#将传入的笔记本列表中的对象在账户中创建
def createAllNotebooks(noteStore,notebooksList):
	for notebook in notebooksList:
		try:
			newNotebook = Types.Notebook()
			newNotebook.name = notebook.name
			newNotebook = noteStore.createNotebook(newNotebook)
		except Exception as e:
			pass
		else:
			pass
		finally:
			pass
#按名查找标签
def findTagByName(tagsList,tagName):
	for tag in tagsList:
		if tag.name == tagName:
			return tag
#按guid查找标签
def findTagByGuid(tagsList,tagGuid):
	for tag in tagsList:
		if tag.guid == tagGuid:
			return tag
#设置标签的上下级关系
def setParentTag(source_tagsList,dest_tagsList):
	for source_tag in source_tagsList:
		if source_tag.parentGuid == None:
			continue
		dest_tag = findTagByName(dest_tagsList, source_tag.name)
		parentTag = findTagByName(dest_tagsList, findTagByGuid(source_tagsList, source_tag.parentGuid).name)
		dest_tag.parentGuid = parentTag.guid
#将更新上下级关系后的标签对象在账户中进行更新
def updateTags(noteStore,tagsList):
	for tag in tagsList:
		noteStore.updateTag(tag)
#将传入的标签列表的对象在账户中进行创建
def createAllTags(noteStore,tagsList):
	for tag in tagsList:
		try:
			newTag = Types.Tag()
			newTag.name = tag.name
			newTag.updateSequenceNum = tag.updateSequenceNum
			noteStore.createTag(newTag)
		except Exception as e:
			pass
		else:
			pass
		finally:
			pass
#获取包括资源等信息的完整笔记
def getFullNote(noteStore,noteGuid):
	return noteStore.getNote(noteGuid, True, True, True, True)
#将传入的笔记对象在账户中进创建
def createNote(noteStore,note):
	noteStore.createNote(note)
#依次复制每个笔记本中的所有笔记
def copyAllNotes(source_noteStore,dest_noteStore,source_notebooksList,dest_notebooksList,source_tagsList,dest_tagsList):
	for notebook in source_notebooksList :
		print 'copying notebook:' + notebook.name
		notesList = getNotesByNotebookGuid(source_noteStore, notebook.guid)
		for note in notesList:
			print '    copying note ' + note.title
			newNote = getFullNote(source_noteStore, note.guid)
			newNote.guid = None
			newNote.notebookGuid = getGuidByNotebookName(notebook.name, dest_notebooksList)
			if newNote.tagGuids != None:
				for i in range(len(newNote.tagGuids)):
					tagGuid = newNote.tagGuids[i]
					newNote.tagGuids[i] = findTagByName(dest_tagsList, findTagByGuid(source_tagsList,tagGuid).name).guid
			createNote(dest_noteStore, newNote)
#源账户初始化
source_client = EvernoteClient(token=source_dev_token,sandbox=False,china=True)
source_userStore = source_client.get_user_store()
source_user = source_userStore.getUser()
source_noteStore = source_client.get_note_store()
#目标账户初始化
dest_client = EvernoteClient(token=dest_dev_token,sandbox=False,china=False)
dest_userStore = dest_client.get_user_store()
dest_user = dest_userStore.getUser()
dest_noteStore = dest_client.get_note_store()
#读取源账户的笔记本列表，并在目标账户中创建相同的笔记本
source_notebooksList = source_noteStore.listNotebooks()
createAllNotebooks(dest_noteStore, source_notebooksList)
dest_notebooksList = dest_noteStore.listNotebooks() 
#读取源账户的标签列表，在目标账户中创建相同的标签，再更新标签的上下级关系
source_tagsList = source_noteStore.listTags()
createAllTags(dest_noteStore, source_tagsList)
dest_tagsList = dest_noteStore.listTags()
setParentTag(source_tagsList, dest_tagsList)
updateTags(dest_noteStore,dest_tagsList)
#复制笔记
copyAllNotes(source_noteStore, dest_noteStore, source_notebooksList, dest_notebooksList, source_tagsList, dest_tagsList)

import ctypes
import ctypes.wintypes as w

OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
SetClipboardData = ctypes.windll.user32.SetClipboardData
SetClipboardData.argtypes = w.UINT, w.HANDLE,
SetClipboardData.restype = w.HANDLE
CloseClipboard = ctypes.windll.user32.CloseClipboard
GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalAlloc.argtypes = w.UINT, w.ctypes.c_size_t,
GlobalAlloc.restype = w.HGLOBAL
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalLock.argtypes = w.HGLOBAL,
GlobalLock.restype = w.LPVOID
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GlobalUnlock.argtypes = w.HGLOBAL,
GlobalUnlock.restype = w.BOOL

GMEM_DDESHARE = 0x2000
CF_UNICODETEXT = 13

def paste(data):
  OpenClipboard(None)
  EmptyClipboard()
  bd = data.encode('utf-16le')
  hCd = GlobalAlloc(GMEM_DDESHARE, len(bd) + 2)
  pchData = GlobalLock(hCd)
  ctypes.memmove(pchData, bd, len(bd))
  GlobalUnlock(hCd)
  SetClipboardData(CF_UNICODETEXT, hCd)
  CloseClipboard()

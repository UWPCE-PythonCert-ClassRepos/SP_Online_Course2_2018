Lesson 09 Assignment - Threaded Downloader
==========================================

by Ross Martin
08/20/2018

If you have a lot of web sites (or web services) to hit at once, you may find that you’re waiting a long time for each request to return.

In that case, your computer isn’t doing much, and it could be waiting on multiple requests all at once.

An option that works well for tens to hundreds of simultaneous connections is threading. Threading works well for this sort of thing as well, because the GIL isn’t a problem – the GIL is released when the system is waiting for a connection to return


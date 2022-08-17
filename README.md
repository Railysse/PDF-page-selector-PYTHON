### What is the project about?

The project is a simple tool I made in Python that can be used to *trim* PDF files. *Trimming* refers to selecting pages from an input PDF file that will be 
exported into another PDF file. It features a simple user interface created with the **tkinter** library (*screenshot below*).

![image](https://user-images.githubusercontent.com/105374710/185097407-07efb3ac-eb44-470a-9c7d-2b81bf0d6177.png)

### What features does it support?

* Choosing a file and folder:

  When selecting the file, the application only shows PDF documents. There is a tick box next to the folder button
  in case you want to export to the same folder as that of the input file.

* Selecting pages:

  Currently, it supports selecting pages by specifying a range and/or by choosing individual pages.
  
* Warnings:

  The UI displays warnings/errors, notifying the user of the following:
  
  - Missing parameters
 
      Not choosing necessary parameters such as *file*, *folder* and/or *pages* will display the specific error when trying to export the file.
 
  - Chosen pages are out of range

      If the input document has, for example, 27 pages and the user selected pages 20 and 30, the application will only export the 20th page and will
      display a warning that some of the chosen pages were left out.
    
  - Success message

    After successfully exporting a file, a message will be displayed in green, inclusing the name of the output document. 

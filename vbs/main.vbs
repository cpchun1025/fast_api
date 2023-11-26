Sub SubmitEntryData()
    Dim wsEntry As Worksheet
    Set wsEntry = ThisWorkbook.Sheets("Entry")
    
    ' Save entry data to file in another folder
    Dim entryData As String
    entryData = wsEntry.Range("A1").Value ' Replace with the actual data range to save
    Dim filePath As String
    filePath = "C:\Path\To\Your\Folder\entry_data.txt" ' Replace with the actual file path
    SaveEntryDataToFile entryData, filePath
    
    ' Call the FastAPI to process the file
    Dim serverURL As String
    serverURL = "http://your-fastapi-url.com/process_file" ' Replace with the actual FastAPI URL
    Dim processedFilePath As String
    processedFilePath = CallFastAPI(filePath, serverURL)
    
    ' Load CSV files into product tabs
    Dim folderPath As String
    folderPath = GetFolderPathFromFastAPIResponse(processedFilePath)
    Dim productTabs() As String
    productTabs = Array("Product_A", "Product_B", "Product_C", "Product_D", "Product_E")
    LoadCSVFilesIntoProductTabs productTabs, folderPath
End Sub

Sub SaveEntryDataToFile(ByVal entryData As String, ByVal filePath As String)
    Open filePath For Output As #1
    Print #1, entryData
    Close #1
End Sub

Function CallFastAPI(ByVal filePath As String, ByVal serverURL As String) As String
    ' Replace with the appropriate code to call the FastAPI with the file path
    ' Send the Excel file to the server
    Dim httpReq As Object
    Set httpReq = CreateObject("MSXML2.XMLHTTP")
    
    With httpReq
        .Open "POST", serverURL, False
        .setRequestHeader "Content-Type", "application/octet-stream"
        .send fileData
        
        ' Check if the request was successful
        If .Status = 200 Then
            ' Save the processed CSV file received from the server
            CallFastAPI = .responseText
        End If
    End With
End Function

Function GetFolderPathFromFastAPIResponse(ByVal savePath As String) As String
    ' Replace with the code to extract the folder path from the FastAPI response
    GetFolderPathFromFastAPIResponse = savePath ' Replace with the actual folder path received from the FastAPI
End Function

Sub LoadCSVFilesIntoProductTabs(ByVal productTabs() As String, ByVal folderPath As String)
    Dim productTab As Variant
    For Each productTab In productTabs
        Dim wsProduct As Worksheet
        Set wsProduct = ThisWorkbook.Sheets(productTab)
        
        Dim productCSVFile As String
        productCSVFile = folderPath & "\" & productTab & ".csv"
        
        If Dir(productCSVFile) <> "" Then
            With wsProduct.QueryTables.Add(Connection:=Array(Array( _
                "TEXT;" & productCSVFile), Array( _
                "UTF-8")), Destination:=wsProduct.Range("A1"))
                .TextFileColumnDataTypes = Array(1) ' Treat all columns as text to preserve formatting
                .TextFileParseType = xlDelimited
                .TextFileCommaDelimiter = True ' Adjust delimiter if necessary
                .Refresh
            End With
        End If
    Next productTab
End Sub
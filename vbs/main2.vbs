Public Sub CallRestApi()

    Const API_URL As String = "http://yourapi.com/process"
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Sheet1") ' Change to your actual sheet name

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row ' Assumes data starts in column A

    Dim httpRequest As Object
    Set httpRequest = CreateObject("MSXML2.XMLHTTP")

    Dim i As Long
    Dim responseData As String
    Dim retryCount As Integer
    Dim maxRetries As Integer: maxRetries = 3 ' Maximum number of retries per row

    For i = 2 To lastRow ' Assumes headers are in the first row
        If ws.Cells(i, "C").Value = "" Then ' Assumes column C is where the result will be stored

            Dim jsonData As String
            jsonData = "{""data"":""" & ws.Cells(i, "A").Value & """}" ' Modify this to match the API's expected format

            retryCount = 0

            Do
                With httpRequest
                    .Open "POST", API_URL, False
                    .setRequestHeader "Content-Type", "application/json"
                    .send jsonData
                    If .Status = 200 Then ' HTTP Status OK
                        responseData = .responseText
                        ws.Cells(i, "C").Value = responseData ' Modify as needed to extract the correct data
                        Exit Do
                    Else
                        retryCount = retryCount + 1
                        If retryCount > maxRetries Then
                            ws.Cells(i, "C").Value = "Failed after " & retryCount & " retries"
                            Exit Do
                        End If
                    End If
                End With
            Loop While retryCount <= maxRetries
        End If
    Next i

    MsgBox "Processing completed."

End Sub
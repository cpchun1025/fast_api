Public Sub CallRestApiWithMultipleFields()

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
        If ws.Cells(i, "N").Value = "" Then ' Assumes column N is where the result will be stored, adjust as needed

            ' Construct JSON from the row's fields
            Dim jsonData As String
            jsonData = "{"
            For j = 1 To 12 ' Assuming 12 fields from column A to L
                jsonData = jsonData & """" & ws.Cells(1, j).Value & """:""" & ws.Cells(i, j).Value & """"
                If j < 12 Then
                    jsonData = jsonData & ","
                End If
            Next j
            jsonData = jsonData & "}"

            retryCount = 0

            Do
                With httpRequest
                    .Open "POST", API_URL, False
                    .setRequestHeader "Content-Type", "application/json"
                    .send jsonData
                    If .Status = 200 Then ' HTTP Status OK
                        responseData = .responseText
                        ws.Cells(i, "N").Value = responseData ' Modify as needed to extract the correct data
                        Exit Do
                    Else
                        retryCount = retryCount + 1
                        If retryCount > maxRetries Then
                            ws.Cells(i, "N").Value = "Failed after " & retryCount & " retries"
                            Exit Do
                        End If
                    End If
                End With
            Loop While retryCount <= maxRetries
        End If
    Next i

    MsgBox "Processing completed."

End Sub
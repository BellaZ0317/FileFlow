# FileFlow API Documentation

Welcome to the **FileFlow API Documentation**.

**Author**: [Bella Zhong](https://github.com/BellaZ0317)

---

## Introduction

**FileFlow** is a lightweight file-sharing web service designed to facilitate quick and easy file sharing between individuals and groups, eliminating the need for user registration or login. By prioritizing convenience, FileFlow allows users to upload and access files using unique numeric identifiers called "spaces." Please note that this convenience comes at the expense of security, as files are accessible to anyone who knows the corresponding space number.

⚠️ **Disclaimer**: FileFlow is intended for temporary and non-sensitive file sharing. Do not use FileFlow to share confidential or sensitive information.

---

## Getting Started

### Base URLs

All API requests should be directed to one of the following base URLs:

**Production Base URL:**

```
http://your-private-fileflow-domain.com
```

**Development Base URL:**

```
http://localhost:4000
```

### No Authentication Required

The FileFlow API does not require any authentication. All endpoints are publicly accessible.

---

## API Overview

FileFlow provides the following functionalities:

- **Upload a File**: Upload a file to a space, optionally specifying a space number.
- **Download a File**: Download a file from a specified space number.
- **Find Available Space**: Retrieve the next available space number for uploading a file.
- **Check Space Availability**: Check if a particular space number is already taken.

---

## API Endpoints

### Summary

| Method | Endpoint                            | Description                                  |
|--------|-------------------------------------|----------------------------------------------|
| `GET`  | `/api/_find_number`                 | Retrieve the next available space number     |
| `GET`  | `/api/_route_taken?space={number}`  | Check if a space number `{number}` is taken  |
| `POST` | `/upload_file`                      | Upload a file to a space                     |
| `GET`  | `/download/{space_number}`          | Download a file from a space                 |

---

### Retrieve Next Available Space Number

Get the next available space number that can be used for uploading a file.

#### **Endpoint**

```http
GET /api/_find_number
```

#### **Response**

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

**Response Body**

```json
{
  "result": 1234
}
```

- `result`: An integer indicating the next available space number.

#### **Example Request**

```bash
curl -X GET http://your-private-fileflow-domain.com/api/_find_number
```

---

### Check Space Availability

Determine whether a specific space number is already taken.

#### **Endpoint**

```http
GET /api/_route_taken?space={space_number}
```

#### **Query Parameters**

- `space` (integer, required): The space number to check.

#### **Response**

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

**Response Body**

```json
{
  "result": true
}
```

- `result`: A boolean value:
  - `true`: The space number is taken.
  - `false`: The space number is available.

#### **Example Request**

Check if space `1234` is taken:

```bash
curl -X GET "http://your-private-fileflow-domain.com/api/_route_taken?space=1234"
```

**Example Response**

If the space is available:

```json
{
  "result": false
}
```

---

### Upload a File

Upload a file to FileFlow, optionally specifying a space number. If the provided space number is unavailable or not provided, the server will assign the next available space number.

#### **Endpoint**

```http
POST /upload_file
```

#### **Form Data Parameters**

- `space` (integer, optional): Desired space number for the file.
- `data_uri` (string, required): The file content encoded as a Data URI (Base64-encoded).

#### **Request Headers**

- `Content-Type`: Should be `application/x-www-form-urlencoded` or `multipart/form-data`.

#### **Response**

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

**Successful Response**

```json
{
  "result": "File uploaded successfully!",
  "upload": true,
  "space": 1234
}
```

- `result`: Success message.
- `upload`: Boolean indicating upload success (`true`).
- `space`: The space number where the file is stored.

**Error Response**

- **Status Code**: `400 Bad Request` or appropriate error code.
- **Content-Type**: `application/json`

```json
{
  "upload": false,
  "error": "File couldn't be uploaded, please try again."
}
```

- `upload`: Boolean indicating upload failure (`false`).
- `error`: Error message.

#### **Example Request**

```bash
curl -X POST http://your-private-fileflow-domain.com/upload_file \
     -F "space=1234" \
     --data-urlencode "data_uri=data:<mime_type>;base64,<base64_encoded_data>"
```

Replace `<mime_type>` with the MIME type of your file (e.g., `image/png`, `text/plain`), and `<base64_encoded_data>` with the Base64-encoded string of your file.

**Note**: If you omit the `space` parameter or if the specified space is taken, the server will assign the next available space number.

#### **Example Successful Response**

```json
{
  "result": "File uploaded successfully!",
  "upload": true,
  "space": 1234
}
```

---

### Download a File

Download a file stored in a specified space number.

#### **Endpoint**

```http
GET /download/{space_number}
```

Replace `{space_number}` with the actual space number.

#### **Response**

- **Status Code**: `200 OK` (if the file exists)
- **Content-Type**: MIME type of the file
- **Body**: Raw file data

**Error Response**

- **Status Code**: `404 Not Found` (if the space number doesn't exist or no file is associated with it)
- **Content-Type**: `application/json`
- **Body**:

```json
{
  "error": "File 1234 doesn't exist."
}
```

#### **Example Request**

```bash
curl -X GET http://your-private-fileflow-domain.com/download/1234 --output downloaded_file
```

This will save the file associated with space number `1234` to `downloaded_file`.

---

## Error Handling

FileFlow uses standard HTTP status codes to indicate the success or failure of an API request. In case of an error, the response will include an `error` message in the body.

### **Common HTTP Status Codes**

- `200 OK`: The request was successful.
- `400 Bad Request`: The request was malformed or missing required parameters.
- `404 Not Found`: The specified space number does not exist or no file is associated with it.
- `500 Internal Server Error`: An unexpected error occurred on the server.

### **Error Response Format**

Error responses are returned in JSON format with an `error` field.

**Example Error Response**

```json
{
  "error": "File 1234 doesn't exist."
}
```

---

## Examples

### Uploading a File

#### **Prerequisites**

- Have the file you wish to upload ready.
- Convert the file to a Base64-encoded Data URI.

#### **Steps**

1. **Check if Desired Space is Available (Optional)**

   This step is optional. If you have a preferred space number, you can check its availability.

   ```bash
   curl -X GET "http://your-private-fileflow-domain.com/api/_route_taken?space=1234"
   ```

   **Response**

   ```json
   {
     "result": false
   }
   ```

   If `result` is `false`, the space is available.

2. **Convert Your File to a Data URI**

   ```bash
   FILE_NAME="your_file.txt"
   MIME_TYPE=$(file --mime-type -b "$FILE_NAME")
   BASE64_DATA=$(base64 -w 0 "$FILE_NAME")
   DATA_URI="data:${MIME_TYPE};base64,${BASE64_DATA}"
   ```

3. **Upload the File**

   ```bash
   curl -X POST http://your-private-fileflow-domain.com/upload_file \
        -F "space=1234" \
        --data-urlencode "data_uri=${DATA_URI}"
   ```

   If you omit the `space` parameter, the server will assign the next available space number.

   **Response**

   ```json
   {
     "result": "File uploaded successfully!",
     "upload": true,
     "space": 1234
   }
   ```

   The file has been uploaded to space number `1234`.

---

### Downloading a File

#### **Steps**

1. **Download the File**

   ```bash
   curl -X GET http://your-private-fileflow-domain.com/download/1234 --output downloaded_file
   ```

   Replace `1234` with the actual space number.

2. **Verify the Downloaded File**

   Compare `downloaded_file` with the original file to ensure they match.

---

## Best Practices and Considerations

- **Security**: Remember that files stored in FileFlow are accessible to anyone with the corresponding space number. Do not upload sensitive or confidential information.

- **Space Numbers**: Space numbers are integers. You can specify a preferred space number when uploading a file; however, if it's already taken, the server will assign the next available space number.

- **Data URI Encoding**: Ensure that the file is correctly converted into a Data URI before uploading. This involves getting the correct MIME type and encoding the file content in Base64.

- **File Size Limitations**: Be mindful of file sizes when using Base64 encoding, as it increases the size of the data by approximately 33%. Consider implementing size limits if necessary.

---

## Contact and Support

For support or inquiries, please reach out to [Bella Zhong](https://github.com/BellaZ0317) or open an issue on the GitHub repository.

---

## Changelog

**Version 1.0**

- Initial release of FileFlow API documentation.

---

## License

This documentation is provided under the MIT License.

---

## Acknowledgments

Thank you for using FileFlow. We appreciate any feedback or contributions to improve this service.

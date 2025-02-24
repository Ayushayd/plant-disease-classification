import { useState, useEffect, useCallback } from "react";
import { styled } from "@mui/material/styles";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Card,
  CardContent,
  Paper,
  CardActionArea,
  CardMedia,
  TableContainer,
  Table,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
  Button,
  CircularProgress,
  Box,
  Stack,
} from "@mui/material";
import { useDropzone } from "react-dropzone";
import ClearIcon from "@mui/icons-material/Clear";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import axios from "axios";
import imageBg from "/bg.png";

const ColorButton = styled(Button)({
  color: "#000",
  backgroundColor: "#fff",
  "&:hover": {
    backgroundColor: "#ffffff7a",
  },
});

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [data, setData] = useState(null);
  const [image, setImage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const sendFile = async () => {
    if (image) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      try {
        console.log("API URL:", import.meta.env.VITE_API_URL); // Debugging
        const res = await axios.post(import.meta.env.VITE_API_URL, formData);
        if (res.status === 200) {
          setData(res.data);
        }
      } catch (error) {
        console.error("Upload failed:", error);
      }
      setIsLoading(false);
    }
  };

  const clearData = () => {
    setData(null);
    setImage(false);
    setSelectedFile(null);
    setPreview(null);
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    if (!preview) return;
    setIsLoading(true);
    sendFile();
  }, [preview]);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length) {
      setSelectedFile(acceptedFiles[0]);
      setData(null);
      setImage(true);
    }
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { "image/*": [] },
    onDrop,
  });

  return (
    <>
      <AppBar
        position="static"
        sx={{ background: "#be6a77", boxShadow: "none", color: "white" }}
      >
        <Toolbar
          sx={{ display: "flex", justifyContent: "center", width: "100%" }}
        >
          <Typography variant="h3" noWrap sx={{ textAlign: "center" }}>
            Plant Type Classification
          </Typography>
        </Toolbar>
      </AppBar>

      <Container
        maxWidth={false}
        sx={{
          backgroundImage: `url(${imageBg})`,
          backgroundRepeat: "no-repeat",
          backgroundPosition: "center",
          backgroundSize: "cover",
          height: "93vh",
          marginTop: "8px",
        }}
      >
        <Stack
          justifyContent="center"
          alignItems="center"
          spacing={2}
          sx={{ padding: "4em 1em 0 1em" }}
        >
          <Box>
            <Card
              sx={{
                maxWidth: 400,
                height: 500,
                margin: "auto",
                borderRadius: 2,
                boxShadow: 3,
              }}
            >
              {image ? (
                <CardActionArea>
                  <CardMedia
                    component="img"
                    height="400"
                    image={preview}
                    alt="Uploaded Preview"
                  />
                </CardActionArea>
              ) : (
                <CardContent>
                  <div
                    {...getRootProps()}
                    style={{
                      border: "2px dashed #be6a77",
                      borderRadius: "12px",
                      padding: "40px",
                      textAlign: "center",
                      cursor: "pointer",
                      background: "linear-gradient(to right, #fce4ec, #f8bbd0)",
                      transition: "all 0.3s ease-in-out",
                      boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.boxShadow =
                        "0px 6px 16px rgba(0, 0, 0, 0.2)")
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.boxShadow =
                        "0px 4px 12px rgba(0, 0, 0, 0.1)")
                    }
                  >
                    <input {...getInputProps()} />
                    <CloudUploadIcon
                      style={{ fontSize: "50px", color: "#be6a77" }}
                    />
                    <Typography
                      variant="h6"
                      color="#333"
                      fontWeight="bold"
                      mt={1}
                    >
                      Drag & drop an image, or click to select
                    </Typography>
                    <Typography variant="body2" color="#555">
                      Supported formats: JPG, PNG, JPEG
                    </Typography>
                  </div>
                </CardContent>
              )}
              {data && (
                <CardContent>
                  <TableContainer
                    component={Paper}
                    sx={{ backgroundColor: "transparent", boxShadow: "none" }}
                  >
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Label:</TableCell>
                          <TableCell align="right">Confidence:</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell>{data.class}</TableCell>
                          <TableCell align="right">
                            {(data.confidence * 100).toFixed(2)}%
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              )}
              {isLoading && (
                <CardContent sx={{ textAlign: "center" }}>
                  <CircularProgress sx={{ color: "#be6a77" }} />
                  <Typography variant="h6">Processing</Typography>
                </CardContent>
              )}
            </Card>
          </Box>
          {data && (
            <Box>
              <ColorButton
                variant="contained"
                size="large"
                onClick={clearData}
                startIcon={<ClearIcon fontSize="large" />}
              >
                Clear
              </ColorButton>
            </Box>
          )}
        </Stack>
      </Container>
    </>
  );
};

export default ImageUpload;

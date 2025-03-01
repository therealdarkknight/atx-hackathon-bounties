import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  styles: {
    global: {
      "html, body, #root": {
        fontFamily:
          "'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif",
        height: "100%",
        margin: "0",
        padding: "0",
        overflow: "hidden",
      },
      ".map-container": {
        position: "absolute",
        top: "0",
        left: "0",
        width: "100%",
        height: "100%",
      },
      ".truck-list": {
        position: "absolute",
        top: "10px",
        left: "10px",
        width: "250px",
        background: "rgba(255, 255, 255, 0.9)",
        padding: "10px",
        borderRadius: "8px",
        boxShadow: "0px 2px 10px rgba(0, 0, 0, 0.2)",
        zIndex: "1000",
        maxHeight: "300px",
        overflowY: "auto",
      },
      ".truck-list h3": {
        marginBottom: "10px",
        fontSize: "18px",
        textAlign: "center",
      },
      ".truck-list ul": {
        listStyle: "none",
        padding: "0",
        margin: "0",
      },
      ".truck-list li": {
        display: "flex",
        alignItems: "center",
        padding: "8px",
        cursor: "pointer",
        borderRadius: "5px",
        transition: "background 0.2s",
        _hover: {
          background: "#f0f0f0",
        },
      },
      ".truck-list .selected": {
        background: "#d1e7ff",
      },
      ".truck-list .icon": {
        width: "20px",
        height: "20px",
        marginRight: "8px",
      },
      ".side-panel": {
        position: "absolute",
        top: "0",
        left: "0",
        width: "200px",
        height: "100vh",
      },
      ".right-sidebar": {
        position: "fixed",
        top: "0",
        right: "0",
        width: "300px",
        maxWidth: "80%",
        height: "100vh",
        backgroundColor: "#fff",
        transform: "translateX(100%)",
        transition: "transform 0.3s ease",
        boxShadow: "-2px 0 5px rgba(0,0,0,0.1)",
        display: "flex",
        flexDirection: "column",
      },
      ".right-sidebar.open": {
        transform: "translateX(0)",
      },
      ".sidebar-header": {
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "#f5f5f5",
        padding: "1rem",
        borderBottom: "1px solid #ddd",
      },
      ".sidebar-header h3": {
        margin: "0",
      },
      ".close-btn": {
        background: "none",
        border: "none",
        cursor: "pointer",
        padding: "4px",
      },
      ".sidebar-content": {
        padding: "1rem",
        overflowY: "auto",
        flex: "1",
      },
    },
  },
});

export default theme;

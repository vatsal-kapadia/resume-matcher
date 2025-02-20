// index.js (Backend for frontend server)   

import express from 'express';  // Using 'import' instead of 'require'
import axios from 'axios';
const app = express();
const port = 3000;

// Serve static HTML files
app.use(express.static("public"));
app.use(express.json());

app.post("/generate", async (req, res) => {
    const { resume, jobDescription } = req.body;

    try {
        // Send POST request to the backend API
        const response = await axios.post("http://127.0.0.1:5000/generate", {
            resume,
            job_description: jobDescription
        });

        // Return the generated resume, cover letter, and alignment score
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: "Failed to generate resume and cover letter." });
    }
});

app.listen(port, () => {
    console.log(`Frontend server is running at http://localhost:${port}`);
});

 






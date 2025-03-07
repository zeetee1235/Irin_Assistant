const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors'); // cors 패키지 추가
const app = express();
const port = 3002;

app.use(cors()); // CORS 미들웨어 추가
app.use(bodyParser.json());
app.use(express.static('src'));

const memoryFilePath = path.join(__dirname, 'memory.json'); // 경로 수정

// Save message endpoint
app.post('/save-message', (req, res) => {
    const { message } = req.body;
    if (!message) {
        return res.status(400).send('Message is required');
    }

    fs.readFile(memoryFilePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading memory file');
        }

        const memory = JSON.parse(data);
        memory.user_input.push(message);

        fs.writeFile(memoryFilePath, JSON.stringify(memory, null, 2), 'utf8', (err) => {
            if (err) {
                return res.status(500).send('Error saving message');
            }

            res.send('Message saved');
        });
    });
});

// Get messages endpoint
app.get('/get-messages', (req, res) => {
    fs.readFile(memoryFilePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading memory file');
        }

        res.send(data);
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
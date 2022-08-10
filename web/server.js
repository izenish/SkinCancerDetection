import express from 'express'
import { spawn } from 'child_process'
import cors from 'cors'
import bodyParser from 'body-parser'
import multer from 'multer'

const app = express()
app.use(cors('*'))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

var storage = multer.diskStorage({
   destination: function (req, file, cb) {
      cb(null, './upload')
   },
   filename: function (req, file, cb) {
      cb(null, file.originalname)
   },
})

let upload = multer({
   storage,
})

app.post('/upload', upload.single('file'), async (req, res) => {
   console.log(req.file)

   if (!req.file) {
      res.json({
         status: 400,
         error: true,
         data: 'Image upload fail in server.',
      })
   }
   res.json({
      status: 200,
      error: false,
      data: 'Image uploaded to server',
   })
})
app.get('/predict', async (req, res) => {
   let pythonRes
   const python = await spawn('python3', ['script.py'])
   python.stdout.on('data', async (data) => {
      pythonRes = data.toString()
   })

   python.on('close', (code) => {
      console.log(`Child Process closed with ${code}`)
      if (code == 0) {
         res.status(200).json({
            status: 200,
            error: false,
            data: pythonRes,
         })
      } else {
         res.status(500).json({
            status: code,
            error: true,
            data: pythonRes,
         })
      }
   })
})

app.listen(8000, () => {
   console.log('Server started at PORT ' + 8000)
})

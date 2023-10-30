import { useState } from 'react';
import { Button } from '@mui/material';
import TextField from '@mui/material/TextField';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [text, setText] = useState("");
  const [exit, setExit] = useState("");

  const handleChange = (e) => {
    e.preventDefault();
    setText(e.target.value);
  }

  const handleFileChange = (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const fileContent = event.target.result;
        setText(fileContent);
      };
      reader.readAsText(file);
    }
  }

  const handleClick = (e) => {
    e.preventDefault();

    setExit("Ejecutando...");
    const data = { entry: text }
    //http://3.88.65.124:8000//api-execute
    fetch(`http://localhost:8000/api-execute`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then((res) => res.json())
      .then((data) => { console.log(data); setExit(data.salida); })
      .catch((error) => { console.log(error); setExit(error); });
  }

  const handleClear = (e) => {
    e.preventDefault();
    setText("");
    setExit("");
  } 

  return (
    <div className='bg-black'>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" 
      integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossOrigin="anonymous"/>
      
      <div className='container'>
      <p className='bg-info' > Componentes - Dashboard</p>
        <div className=''>
        <TextField className='bg-light'
        onChange={handleFileChange}
        helperText="Archivo a ejecutar"
        type='file'
        inputProps={{
          accept: '*/*'
        }}
        fullWidth
      />
      <br /> <br />
        </div>
        <div className='border-bottom border-info'>
        <p className='bg-info'>Consola</p>
      <TextField className='bg-light'
       
        label="Comandos a Ejecutar"
        multiline
        minRows={10}
        maxRows={10}
        fullWidth
        onChange={handleChange}
        value={text}
      />
      <br /> <br /> <br />
      <div style={{ display: "flex", gap: 10 }}>
        <Button variant="contained" onClick={handleClick}>Ejecutar</Button>
        <Button variant="contained" onClick={handleClear}>Limpiar</Button>
      </div>
        </div>
        

      <br /> 

      <p className='bg-info'>Salida</p>
      <TextField className='bg-light'
        label="Salida comandos"
        multiline
        minRows={10}
        maxRows={10}
        fullWidth
        value={exit}
        disabled={true}
      />

      <br /> <br /> <br />

      <Link to="/login">
        <Button variant="outlined" color="error">Ir a Login</Button>
      </Link>
      </div>

      

      

      

      
    </div>
  )
}
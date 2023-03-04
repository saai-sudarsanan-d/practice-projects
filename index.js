const btn = document.getElementById("btn")
const color = document.querySelector(".color")
btn.addEventListener('click',
    ()=>{
        const R = Math.floor(Math.random() * (255 - 0 + 1));
        const G = Math.floor(Math.random() * (255 - 0 + 1));
        const B = Math.floor(Math.random() * (255 - 0 + 1));
        const c = `rgb(${R},${G},${B})`
        document.body.style.backgroundColor = c;
        color.textContent = c;
    }
);
const copy = document.querySelector(".container h2");
copy.addEventListener('click',
    ()=>{
        let content = color.textContent;
        navigator.clipboard.writeText(content);
        alert(`Copied : ${content}`);
    }
);
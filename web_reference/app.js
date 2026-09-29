const sidebar=document.getElementById('sidebar');
const aiPanel=document.getElementById('aiPanel');
const backdrop=document.getElementById('backdrop');
const menuBtn=document.getElementById('menuBtn');
const aiBtn=document.getElementById('aiBtn');
const closeAi=document.getElementById('closeAi');

function openSidebar(){sidebar.classList.add('open'); backdrop.classList.add('show')}
function openAI(){aiPanel.classList.add('open'); backdrop.classList.add('show')}
function closeDrawers(){sidebar.classList.remove('open'); aiPanel.classList.remove('open'); backdrop.classList.remove('show')}

menuBtn?.addEventListener('click',openSidebar);
aiBtn?.addEventListener('click',openAI);
closeAi?.addEventListener('click',closeDrawers);
backdrop?.addEventListener('click',closeDrawers);

document.querySelectorAll('.nav-item').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    if(window.innerWidth<=768) closeDrawers();
  });
});

document.getElementById('sendBtn')?.addEventListener('click',()=>{
  const input=document.getElementById('chatInput');
  const text=input.value.trim();
  if(!text)return;
  const chat=document.querySelector('.chat');
  const msg=document.createElement('div');
  msg.className='message user';
  msg.innerHTML=`<div>${text.replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]))}</div>`;
  chat.appendChild(msg);
  input.value='';
  chat.scrollTop=chat.scrollHeight;
});
document.getElementById('chatInput')?.addEventListener('keydown',e=>{
  if(e.key==='Enter') document.getElementById('sendBtn').click();
});
window.addEventListener('resize',()=>{
  if(window.innerWidth>768) closeDrawers();
});

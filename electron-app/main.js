const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');
const { execSync, exec } = require('child_process');
const fs = require('fs');
const waitOn = require('wait-on');

let mainWindow;
let djangoProcess = null; // Store Django process

function ensureDatabase() {
    const isPackaged = app.isPackaged;
    const resourcesPath = isPackaged ? process.resourcesPath : path.join(__dirname, '..');
    const DATABASE_SOURCE = isPackaged 
        ? path.join(resourcesPath, 'db.sqlite3') 
        : path.join(__dirname, '..', 'db.sqlite3');
    const DATABASE_DESTINATION = path.join(resourcesPath, 'db.sqlite3');

    try {
        if (!fs.existsSync(DATABASE_DESTINATION)) {
            console.log("⚡ Copying default db.sqlite3...");
            fs.copyFileSync(DATABASE_SOURCE, DATABASE_DESTINATION);
            console.log("✅ Database copied successfully.");
        } else {
            console.log("🔄 Database already exists, skipping copy.");
        }
    } catch (error) {
        console.error(`❌ Failed to copy database: ${error.message}`);
    }
}

function ensureVenv() {
    const isPackaged = app.isPackaged;
    const resourcesPath = isPackaged ? process.resourcesPath : __dirname;
    const VENV_DIR = path.join(resourcesPath, 'venv');
    const PYTHON_EXECUTABLE = path.join(VENV_DIR, 'bin', 'python3');
    const REQUIREMENTS_FILE = path.join(resourcesPath, 'requirements.txt');

    console.log(`🔍 Checking virtual environment at: ${VENV_DIR}`);

    try {
        if (!fs.existsSync(PYTHON_EXECUTABLE)) {
            console.log("⚡ Virtual environment not found. Creating...");
            execSync(`python3 -m venv ${VENV_DIR}`, { stdio: 'inherit' });
            console.log("✅ Virtual environment created.");

            console.log("⬆️ Upgrading pip...");
            execSync(`${PYTHON_EXECUTABLE} -m pip install --upgrade pip`, { stdio: 'inherit' });

            if (fs.existsSync(REQUIREMENTS_FILE)) {
                console.log("📦 Installing dependencies...");
                execSync(`${PYTHON_EXECUTABLE} -m pip install -r ${REQUIREMENTS_FILE}`, { stdio: 'inherit' });
                console.log("🚀 Dependencies installed.");
            } else {
                console.warn(`⚠️ Warning: ${REQUIREMENTS_FILE} not found. Skipping dependency installation.`);
            }
        } else {
            console.log("🔄 Virtual environment already exists.");
        }
    } catch (error) {
        console.error(`❌ Failed to set up virtual environment: ${error.message}`);
        app.quit();
    }
}

function applyMigrations() {
    const isPackaged = app.isPackaged;
    const resourcesPath = isPackaged ? process.resourcesPath : __dirname;
    const PYTHON_EXECUTABLE = path.join(resourcesPath, 'venv', 'bin', 'python3');
    const DJANGO_PROJECT_PATH = isPackaged ? path.join(resourcesPath, 'app') : path.join(__dirname, '..');

    console.log("📂 Applying database migrations...");
    try {
        execSync(`${PYTHON_EXECUTABLE} ${DJANGO_PROJECT_PATH}/manage.py migrate`, { cwd: DJANGO_PROJECT_PATH, stdio: 'inherit' });
        console.log("✅ Database migrations applied successfully.");
    } catch (error) {
        console.error(`❌ Error applying migrations: ${error.message}`);
    }
}

// 🛑 **Create Django Superuser**
function createSuperUser() {
    const isPackaged = app.isPackaged;
    const resourcesPath = isPackaged ? process.resourcesPath : __dirname;
    const PYTHON_EXECUTABLE = path.join(resourcesPath, 'venv', 'bin', 'python3');
    const DJANGO_PROJECT_PATH = isPackaged ? path.join(resourcesPath, 'app') : path.join(__dirname, '..');

    console.log("👤 Checking if superuser exists...");

    const createSuperUserCommand = `${PYTHON_EXECUTABLE} ${DJANGO_PROJECT_PATH}/manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Zero@1933')
    print('✅ Superuser created successfully!')
else:
    print('🔄 Superuser already exists, skipping.')
"`;

    try {
        execSync(createSuperUserCommand, { cwd: DJANGO_PROJECT_PATH, stdio: 'inherit' });
    } catch (error) {
        console.error(`❌ Failed to create superuser: ${error.message}`);
    }
}

function startDjangoServer() {
    const isPackaged = app.isPackaged;
    const resourcesPath = isPackaged ? process.resourcesPath : __dirname;
    const PYTHON_EXECUTABLE = path.join(resourcesPath, 'venv', 'bin', 'python3');
    const DJANGO_PROJECT_PATH = isPackaged ? path.join(resourcesPath, 'app') : path.join(__dirname, '..');

    console.log("🚀 Starting Django server...");

    djangoProcess = exec(`${PYTHON_EXECUTABLE} ${DJANGO_PROJECT_PATH}/manage.py runserver 8000`,
        { cwd: DJANGO_PROJECT_PATH },
        (error, stdout, stderr) => {
            if (error) {
                console.error(`❌ Error starting Django: ${error.message}`);
                return;
            }
            console.log(`📜 Django output: ${stdout}`);
            if (stderr) console.error(`⚠️ Django stderr: ${stderr}`);
        }
    );

    djangoProcess.on('exit', (code) => {
        console.log(`🔴 Django process exited with code ${code}`);
    });
}

// 🛑 **Kill Django & Electron when the app exits**
function cleanup() {
    console.log("🛑 Cleaning up Django process before quitting...");
    if (djangoProcess) {
        djangoProcess.kill();
    }

    console.log("🛑 Killing Electron process...");
    app.quit();
    process.exit(0);
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false  // ✅ Required for clipboard operations
        }
    });

    ensureDatabase();
    ensureVenv();
    applyMigrations();

    // **Give Django time to start before creating superuser**
    setTimeout(() => {
        createSuperUser();
    }, 3000); 

    startDjangoServer();

    console.log("⏳ Waiting for Django to start...");

    waitOn({ resources: ['http://127.0.0.1:8000/accounts/login/'] })
        .then(() => {
            console.log("✅ Django server is ready. Loading login page...");
            mainWindow.loadURL('http://127.0.0.1:8000/accounts/login/');
        })
        .catch((err) => {
            console.error('❌ Django server failed to start:', err);
        });

    // ✅ Enable Right-Click Copy-Paste Menu
    mainWindow.webContents.on('context-menu', (event, params) => {
        const contextMenu = Menu.buildFromTemplate([
            { role: 'cut' },
            { role: 'copy' },
            { role: 'paste' },
            { role: 'selectAll' }
        ]);
        contextMenu.popup();
    });

    // ✅ Kill Django & Electron when window closes
    mainWindow.on('closed', () => {
        cleanup();
    });

    // ✅ Print Handler
    ipcMain.on('print-page', (event) => {
        if (mainWindow) {
            console.log("🖨️ Printing expense page...");
            mainWindow.webContents.print({ silent: false, printBackground: true });
        }
    });

    // ✅ Add File Menu with Clipboard and Print
    const menuTemplate = [
        {
            label: 'File',
            submenu: [
                { role: 'undo' },
                { role: 'redo' },
                { type: 'separator' },
                { role: 'cut' },
                { role: 'copy' },
                { role: 'paste' },
                { role: 'selectAll' },
                { type: 'separator' },
                {
                    label: 'Print',
                    accelerator: 'CmdOrCtrl+P',
                    click: () => {
                        mainWindow.webContents.print({ silent: false, printBackground: true });
                    }
                },
                { type: 'separator' },
                {
                    label: 'Quit',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        cleanup();
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(menuTemplate);
    Menu.setApplicationMenu(menu);
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => cleanup());
app.on('quit', () => cleanup());
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
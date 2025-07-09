module.exports = {
    apps: [
        {
            name: "contador_es",
            script: "manage.py",
            interpreter: "env/Scripts/python.exe",
            args: "runserver 0.0.0.0:8000",
            watch: false
        }
    ]
}
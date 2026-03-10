local stuff = {
    earth = "Celestial Body : Crashed with Theia.",
    theia = function(crashObj)
         if crashObj == "earth" then
            print("Crashed 4.5 billion years from now.")
        end
    end
}
local sf = stuff

sf.theia("earth")
print(sf.earth)
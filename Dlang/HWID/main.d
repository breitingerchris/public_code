module main;

import std.stdio;
import std.conv;
import std.file;
import core.thread;
import core.sys.windows.windows;
import std.digest.md;

int main(string[] args)
{

	core.sys.windows.windows.SYSTEM_INFO sys;
	GetNativeSystemInfo(&sys);
	auto hwidstring = to!string(sys.dwOemId) ~ to!string(sys.dwNumberOfProcessors) ~ to!string(sys.dwProcessorType);
	auto hwid = toHexString(md5Of(to!string(hwidstring)));
	std.file.write("hwid.txt", hwid);
	writeln("HWID Written to hwid.txt!");
	core.thread.Thread.sleep(dur!("seconds")(3));
	return 0;
}
